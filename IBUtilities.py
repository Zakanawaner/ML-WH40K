import requests
import trimesh
import io


# This function gets the info from each squad on the Roster XML file
def ib_utilities_get_squad_info(root_select):
    keys = []
    faction_keys = []
    for key_ in root_select.find('p', attrs={'class': 'category-names'}).find_all('span')[1].text.strip().split(', '):
        faction_keys.append(key_) if 'Faction' in key_ else keys.append(key_)
    rule = root_select.find('p', attrs={'class': 'rule-names'}).find_all('span')[1].text.strip().split(', ') if root_select.find('p', attrs={'class': 'rule-names'}) is not None else []
    abilities_unit = None
    powers_unit = None
    psyker_unit = None
    stats_unit = None
    weapon_unit = None
    for table in root_select.find_all('table'):
        if table.find('th').text.strip() == 'Abilities':
            abilities_unit = [ability.text.strip() for ability in table.find_all('td')]
        if table.find('th').text.strip() == 'Psychic Power':
            powers_unit = [stat.text.strip() for stat in table.find_all('td')]
        if table.find('th').text.strip() == 'Psyker':
            psyker_unit = [stat.text.strip() for stat in table.find_all('td')]
        if table.find('th').text.strip() == 'Unit':
            stats_unit = [stat.text.strip() for stat in table.find_all('td')]
        if table.find('th').text.strip() == 'Weapon':
            weapon_unit = [stat.text.strip() for stat in table.find_all('td')]
    if root_select.find('ul') is not None:
        list_ = root_select.find('ul').find_all('li')
    else:
        list_ = [root_select]
    units_in_squad = []
    for number in list_:
        unit_in_squad = {}
        for i, num in enumerate(number.find('p', attrs={'class': 'profile-names'}).find_all('span')):
            if 'Unit' in num.text.strip():
                unit_in_squad['Nickname'] = number.find('p', attrs={'class': 'profile-names'}).find_all('span')[i + 1].text.strip()
                unit_in_squad['Stats'] = {
                    'M': stats_unit[stats_unit.index(unit_in_squad['Nickname']) + 1],
                    'WS': stats_unit[stats_unit.index(unit_in_squad['Nickname']) + 2],
                    'BS': stats_unit[stats_unit.index(unit_in_squad['Nickname']) + 3],
                    'S': stats_unit[stats_unit.index(unit_in_squad['Nickname']) + 4],
                    'T': stats_unit[stats_unit.index(unit_in_squad['Nickname']) + 5],
                    'W': stats_unit[stats_unit.index(unit_in_squad['Nickname']) + 6],
                    'A': stats_unit[stats_unit.index(unit_in_squad['Nickname']) + 7],
                    'Ld': stats_unit[stats_unit.index(unit_in_squad['Nickname']) + 8],
                    'Sv': stats_unit[stats_unit.index(unit_in_squad['Nickname']) + 9]
                }
            if 'Weapon' in num.text.strip():
                unit_in_squad['Weapons'] = []
                weapon_list = number.find('p', attrs={'class': 'profile-names'}).find_all('span')[i + 1].text.strip().split(', ')
                weapon_list = ib_utilities_exception_guns(weapon_list)
                for weapon in weapon_list:
                    unit_in_squad['Weapons'].append({
                        'Name': weapon,
                        'Range': weapon_unit[weapon_unit.index(weapon) + 1],
                        'Type': weapon_unit[weapon_unit.index(weapon) + 2],
                        'S': weapon_unit[weapon_unit.index(weapon) + 3],
                        'AP': weapon_unit[weapon_unit.index(weapon) + 4],
                        'D': weapon_unit[weapon_unit.index(weapon) + 5],
                        'Abilities': weapon_unit[weapon_unit.index(weapon) + 6],
                    })
        if 'Nickname' not in unit_in_squad.keys():
            unit_in_squad['Nickname'] = stats_unit[0]
            unit_in_squad['Stats'] = {
                'M': stats_unit[1],
                'WS': stats_unit[2],
                'BS': stats_unit[3],
                'S': stats_unit[4],
                'T': stats_unit[5],
                'W': stats_unit[6],
                'A': stats_unit[7],
                'Ld': stats_unit[8],
                'Sv': stats_unit[9]
            }
        if 'Weapons' not in unit_in_squad.keys():
            unit_in_squad['Weapons'] = [{
                'Name': weapon_unit[8 * i + 1],
                'Range': weapon_unit[8 * i + 2],
                'Type': weapon_unit[8 * i + 3],
                'S': weapon_unit[8 * i + 4],
                'AP': weapon_unit[8 * i + 5],
                'D': weapon_unit[8 * i + 6],
                'Abilities': weapon_unit[8 * i + 7],
            } for i in range(int(len(weapon_unit)/8))]
        if number.find('h4').text.strip().find('x ') != -1:
            number_unit = int(number.text.strip()[:number.text.strip().find('x ')])
        else:
            number_unit = 1
        unit_in_squad['Abilities'] = [{
            'Name': abilities_unit[i * 3],
            'Description': abilities_unit[i * 3 + 1],
        } for i in range(int(len(abilities_unit) / 3))] if abilities_unit is not None else []
        unit_in_squad['Psyker'] = {
            'Type': psyker_unit[0],
            'Cast': psyker_unit[1],
            'Deny': psyker_unit[2],
            'Powers_known': psyker_unit[3],
        } if psyker_unit is not None else []
        unit_in_squad['PsychicPowers'] = [{
            'Name': powers_unit[i * 5],
            'Warp_charge': powers_unit[i * 5 + 1],
            'Range': powers_unit[i * 5 + 2],
            'Details': powers_unit[i * 5 + 2],
        } for i in range(int(len(powers_unit) / 5))] if powers_unit is not None else []
        for i in range(number_unit):
            units_in_squad.append(unit_in_squad)
    return units_in_squad, stats_unit, rule, faction_keys, keys


# Exceptions guns (to be completed). Function for dealing with composed weapons names separated with comma
def ib_utilities_exception_guns(list_):
    done = False
    while not done:
        done = True
        if 'Standard' in list_:
            list_[list_.index('Standard') - 1] = list_[list_.index(
                'Standard') - 1] + ', ' + 'Standard'
            list_.pop(list_.index('Standard'))
            done = False
        if 'Supercharge' in list_:
            list_[list_.index('Supercharge') - 1] = list_[list_.index(
                'Supercharge') - 1] + ', ' + 'Supercharge'
            list_.pop(list_.index('Supercharge'))
            done = False
    done = False
    while not done:
        done = True
        if 'Missile launcher' in list_ and 'missile' in list_[list_.index('Missile launcher') + 1]:
            index = list_.index('Missile launcher')
            list_[list_.index('Missile launcher')] = list_[list_.index('Missile launcher')] + ', ' + list_[list_.index('Missile launcher') + 1]
            list_.pop(index + 1)
            done = False
    return list_


# Function that finds the object in the database. To be completed with the exceptions
def ib_utilities_check_names(model_name, db_names):
    if model_name in db_names:
        model_names = [i for i, name in enumerate(db_names) if name == model_name]
        return model_names
    else:
        for i, c in enumerate(model_name.replace('-', ' ')):
            if c.isdigit():
                model_name = model_name[:i]
                break
            elif c == '/':
                index = i
                for k in range(i, 0, -1):
                    if model_name[k] == ' ':
                        index = k
                        break
                model_name = model_name[:index]
                break
            elif c == '(':
                index = i
                for k in range(i, 0, -1):
                    if model_name[k] == ' ':
                        index = k
                        break
                model_name = model_name[:index]
                break
        if model_name.lower().replace('-', '').replace(' ', '').replace('/', '') in db_names:
            model_names = [i for i, name in enumerate(db_names) if name == model_name.lower().replace('-', '').replace(' ', '').replace('/', '')]
            return model_names
        print("Problem with this guy's Roster Name: " + model_name)
        return []


# Function that returns the minimum cylinder of the 3D model
def ib_utilities_get_cylinder_bounds(model):
    model_obj = io.StringIO(requests.get(model['CustomMesh']['MeshURL']).content.decode('utf-8'))
    mesh = trimesh.load_mesh(file_obj=model_obj, file_type='obj')
    return {
        'radius': trimesh.bounds.minimum_cylinder(mesh)['radius'] * model['Transform']['scaleX'],
        'height': trimesh.bounds.minimum_cylinder(mesh)['height'] * model['Transform']['scaleX']
    }


# Function that handles the structure of the arm dictionary when called by IB
def ib_utilities_get_categories(types, category, army, cls=False):
    if cls:
        army[types] = {
            'Meta': category.find('h3').text.strip(),
            'List': []
        }
        for root_select in category.find_all('li', attrs={'class': 'rootselection'}):
            army[types]['List'].append({
                'Name': root_select.find('h4').text.strip(),
                'Selection': root_select.find('p').text.strip()
            })
    else:
        army[types] = {
            'Meta': category.find('h3').text.strip(),
            'Squads': []
        }
        for root_select in category.find_all('li', attrs={'class': 'rootselection'}):
            units_in_squad, stats_unit, rule, faction_keys, keys = ib_utilities_get_squad_info(root_select)
            army[types]['Squads'].append({
                'SquadName': stats_unit[0],
                'Units': units_in_squad,
                'Rules': rule,
                'FactionKeys': faction_keys,
                'Keys': keys
            })
    return army

