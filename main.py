import glob
import json
from xml_handler import dict_to_xml, xml_to_string, pretty_print_xml, save_pretty_xml_to_file, read_xml


def unit_artdef(folder, config):
    artdef_units = config['units_specified']
    artdef_name = 'Units.artdef'
    artdefs = [f for f in glob.glob(f'{folder}/**/*{artdef_name}*', recursive=True)]
    if len(artdefs) == 0:
        raise FileNotFoundError(f'No files were found that match Units.artdef. Make sure your config.json points to your civ VI directory.')

    artdef_info = read_xml(artdefs[0])
    artdef_info_ = artdef_info['AssetObjects..ArtDefSet']['m_RootCollections']['Element']
    full_artdef = {i['m_CollectionName']['@text']: i.get('Element', []) for i in artdef_info_}

    for artdef in artdefs[1:]:
        artdef_info = read_xml(artdef)
        artdef_info_ = artdef_info['AssetObjects..ArtDefSet']['m_RootCollections']['Element']
        artdef_dict = {i['m_CollectionName']['@text']: i['Element'] for i in artdef_info_ if
                       i.get('Element', None) is not None}

        for i, j in artdef_dict.items():
            if isinstance(j, dict):
                full_artdef[i].append(j)
            elif isinstance(j, list):
                full_artdef[i].extend(j)
            else:
                print('weird collection')

    uniques = []
    not_uniques = []
    drop_indices = []
    for idx, i in enumerate(full_artdef['Units']):
        if i['m_Name']['@text'] not in uniques:
            uniques.append(i['m_Name']['@text'])
        else:
            not_uniques.append(i)
            drop_indices.append(idx)

    drop_indices.reverse()
    for i in drop_indices:
        del full_artdef['Units'][i]

    artdef_total = {i['m_Name']['@text']: i for i in full_artdef['Units']}
    # reset scout, warrior, due to the scout cat pack, and the zombies pack
    artdef_total['UNIT_SCOUT'] = [i for i in not_uniques if 'SCOUT' in i['m_Name']['@text']][0]
    artdef_total['UNIT_WARRIOR'] = [i for i in not_uniques if 'WARRIOR' in i['m_Name']['@text']][0]
    artdef_template = read_xml('Units_template.artdef')
    artdef_template['AssetObjects..ArtDefSet']['m_RootCollections']['Element']['Element'] = []
    root = artdef_template['AssetObjects..ArtDefSet']['m_RootCollections']['Element']['Element']

    failed = {'multsearch': [], 'nosearch': []}
    search_found = []
    used = []
    for mod_ref, vanilla_ref in artdef_units.items():
        if artdef_total.get(vanilla_ref) is None:
            search = [i for i in artdef_total if vanilla_ref.replace('UNIT_', '') in i]
            if len(search) > 1:
                root.append(assign_artdef(artdef_total[search[0]], mod_ref))
                print(f'found more than one match for {vanilla_ref}, using the first found.')
                failed['multsearch'].append(artdef_units[mod_ref])
                used.append(vanilla_ref)
            elif len(search) == 0:
                print(f'no match for {vanilla_ref}')
                failed['nosearch'].append(artdef_units[mod_ref])
            else:
                root.append(assign_artdef(artdef_total[search[0]], mod_ref))
                search_found.append(artdef_units[mod_ref])
                used.append(vanilla_ref)
                print(f'Found partial match for specified {vanilla_ref}. {mod_ref} now uses {search[0]}')
        else:
            root.append(assign_artdef(artdef_total[vanilla_ref], mod_ref))
            used.append(vanilla_ref)
            print(f"Success! {mod_ref} now uses {artdef_total[vanilla_ref]['m_Name']['@text']}")

    # remake the weird formation
    #artdef_template['AssetObjects::ArtDefSet'] = artdef_template.pop('AssetObjects')
    root = dict_to_xml(artdef_template)
    xml_string = xml_to_string(root)
    pretty_xml_string = pretty_print_xml(xml_string)
    save_pretty_xml_to_file(pretty_xml_string, artdef_name)

    print(f'Saved unit mapping to {artdef_name}. Import it into modbuddy and you should be able to build with it.')
    if config["show_all_possible_units"]:
        total_units = set([i for i in artdef_total])
        unused = list(total_units - set(used))
        print('Here are all the other units you could have used (although some are scenario only):')
        print(f"{unused}")
    else:
        print('If you want to see the list of units you could use, set config.jsons "show_all_possible_units" to true.')


def assign_artdef(artdef, name):
    artdef_cpy = artdef.copy()
    artdef_cpy['m_Name'] = {'@text': name}
    return artdef_cpy


def main():
    with open("config.json", 'r') as json_file:
        config = json.load(json_file)
    folder = config.get('civ_install', None)
    if folder == "YOUR_DIRECTORY_HERE":
        raise FileNotFoundError(
            "Set your civ VI install filepath in config.json.")

    unit_artdef(folder, config)


if __name__ == "__main__":
    main()
