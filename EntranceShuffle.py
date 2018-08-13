import random

def link_entrances(world):

    # setup mandatory connections
    for exitname, regionname in mandatory_connections:
        connect_simple(world, exitname, regionname)

    # if we do not shuffle, set default connections
    if world.shuffle == 'vanilla':
        for exitname, regionname in default_connections:
            connect_simple(world, exitname, regionname)
        for exitname, regionname in default_dungeon_connections:
            connect_simple(world, exitname, regionname)
    else:
        raise NotImplementedError('Shuffling not supported yet')


def connect_simple(world, exitname, regionname):
    world.get_entrance(exitname).connect(world.get_region(regionname))

def connect_entrance(world, entrancename, exitname):
    entrance = world.get_entrance(entrancename)
    # check if we got an entrance or a region to connect to
    try:
        region = world.get_region(exitname)
        exit = None
    except RuntimeError:
        exit = world.get_entrance(exitname)
        region = exit.parent_region

    # if this was already connected somewhere, remove the backreference
    if entrance.connected_region is not None:
        entrance.connected_region.entrances.remove(entrance)

    target = exit_ids[exit.name][0] if exit is not None else exit_ids.get(region.name, None)
    addresses = door_addresses[entrance.name][0]

    entrance.connect(region, addresses, target)
    world.spoiler.set_entrance(entrance.name, exit.name if exit is not None else region.name, 'entrance')


def connect_exit(world, exitname, entrancename):
    entrance = world.get_entrance(entrancename)
    exit = world.get_entrance(exitname)

    # if this was already connected somewhere, remove the backreference
    if exit.connected_region is not None:
        exit.connected_region.entrances.remove(exit)

    exit.connect(entrance.parent_region, door_addresses[entrance.name][1], exit_ids[exit.name][1])
    world.spoiler.set_entrance(entrance.name, exit.name, 'exit')


def connect_random(world, exitlist, targetlist, two_way=False):
    targetlist = list(targetlist)
    random.shuffle(targetlist)

    for exit, target in zip(exitlist, targetlist):
        if two_way:
            connect_two_way(world, exit, target)
        else:
            connect_entrance(world, exit, target)


def connect_doors(world, doors, targets):
    """This works inplace"""
    random.shuffle(doors)
    random.shuffle(targets)
    while doors:
        door = doors.pop()
        target = targets.pop()
        connect_entrance(world, door, target)

# these are connections that cannot be shuffled and always exist. They link together separate parts of the world we need to divide into regions
mandatory_connections = [('Links House Spawn', 'Links House Child'),
#                        ('Temple of Time Spawn', ' Temple of Time Adult'), # Unused
                         ('Mido House Child to Shared', 'Mido House Shared'),
                         ('Mido House Adult to Shared', 'Mido House Shared'),
                         ('Kokiri Forest Storms Grotto Child to Shared', 'Kokiri Forest Storms Grotto Shared'),
                         ('Kokiri Forest Storms Grotto Adult to Shared', 'Kokiri Forest Storms Grotto Shared'),
                         ('Lost Woods Ocarina Child to Shared', 'Lost Woods Ocarina Shared'),
                         ('Lost Woods Ocarina Adult to Shared', 'Lost Woods Ocarina Shared'),
                         ('Lost Woods Bridge Child', 'Lost Woods Bridge Child'),
                         ('Lost Woods Bridge Adult', 'Lost Woods Bridge Adult'),
			 ('Lost Woods Ladder Adult', 'Lost Woods Adult'),
			 ('Lost Woods Bridge Jump Adult', 'Lost Woods Bridge Adult'),
			 ('Lost Woods Past Mido Adult', 'Lost Woods Past Mido Adult'),
			 ('Lost Woods Mido Pass Reverse Adult', 'Lost Woods Adult'),
                         ('Lost Woods Generic Grotto Child to Shared', 'Lost Woods Generic Grotto Shared'),
                         ('Lost Woods Generic Grotto Adult to Shared', 'Lost Woods Generic Grotto Shared'),
                         ('Lost Woods Sales Grotto Child to Shared', 'Lost Woods Sales Grotto Shared'),
                         ('Lost Woods Sales Grotto Adult to Shared', 'Lost Woods Sales Grotto Shared'),
                         ('Meadow Wolfos Grotto Child to Shared', 'Meadow Wolfos Grotto Shared'),
                         ('Meadow Wolfos Grotto Adult to Shared', 'Meadow Wolfos Grotto Shared'),
                         ('Remote Southern Grotto Child to Shared', 'Remote Southern Grotto Shared'),
                         ('Remote Southern Grotto Adult to Shared', 'Remote Southern Grotto Shared'),
                         ('Field Near Lake Outside Fence Grotto Child to Shared', 'Field Near Lake Outside Fence Grotto Shared'),
                         ('Field Near Lake Outside Fence Grotto Adult to Shared', 'Field Near Lake Outside Fence Grotto Shared'),
                         ('Field Near Lake Inside Fence Grotto Child to Shared', 'Field Near Lake Inside Fence Grotto Shared'),
                         ('Field Near Lake Inside Fence Grotto Adult to Shared', 'Field Near Lake Inside Fence Grotto Shared'),
                         ('Field Near Valley Grotto Child to Shared', 'Field Near Valley Grotto Shared'),
                         ('Field Near Valley Grotto Adult to Shared', 'Field Near Valley Grotto Shared'),
                         ('Field West Castle Town Grotto Child to Shared', 'Field West Castle Town Grotto Shared'),
                         ('Field West Castle Town Grotto Adult to Shared', 'Field West Castle Town Grotto Shared'),
                         ('Field Near Kakariko Grotto Child to Shared', 'Field Near Kakariko Grotto Shared'),
                         ('Field Near Kakariko Grotto Adult to Shared', 'Field Near Kakariko Grotto Shared'),
                         ('Field North of Lon Lon Grotto Child to Shared', 'Field North of Lon Lon Grotto Shared'),
                         ('Field North of Lon Lon Grotto Adult to Shared', 'Field North of Lon Lon Grotto Shared'),
                         ('Zora River Rocks Child', 'Zora River Top Child'),
                         ('Zora River Downstream Child', 'Zora River Bottom Child'),
                         ('Zora River Child to Shared', 'Zora River Shared'),
                         ('Zora River Adult to Shared', 'Zora River Shared'),
                         ('Zora River Plateau Open Grotto Child to Shared', 'Zora River Plateau Open Grotto Shared'),
                         ('Zora River Plateau Open Grotto Adult to Shared', 'Zora River Plateau Open Grotto Shared'),
                         ('Zoras Fountain Fairy Child to Shared', 'Zoras Fountain Fairy Shared'),
                         ('Zoras Fountain Fairy Adult to Shared', 'Zoras Fountain Fairy Shared'),
                         ('Lake Hylia Lab Child to Shared', 'Lake Hylia Lab Shared'),
                         ('Lake Hylia Lab Adult to Shared', 'Lake Hylia Lab Shared'),
                         ('Gerudo Valley Crate PoH Child to Shared', 'Gerudo Valley Crate PoH Shared'),
                         ('Gerudo Valley Crate PoH Adult to Shared', 'Gerudo Valley Crate PoH Shared'),
                         ('Gerudo Valley Waterfall PoH Child to Shared', 'Gerudo Valley Waterfall PoH Shared'),
                         ('Gerudo Valley Waterfall PoH Adult to Shared', 'Gerudo Valley Waterfall PoH Shared'),
                         ('Gerudo Valley Waterfall PoH Far Side Adult to Shared', 'Gerudo Valley Waterfall PoH Shared'),
                         ('Gerudo Bridge Adult', 'Gerudo Valley Far Side Adult'),
#                        ('Gerudo Bridge Reverse Child', 'Gerudo Valley Child'),
                         ('Gerudo Bridge Reverse Adult', 'Gerudo Valley Adult'),
                         ('Gerudo Valley Silver Rock Adult', 'Gerudo Valley Silver Rock Adult'),
                         ('Fortress Bottom to Middle Adult', 'Fortress Middle Level Adult'),
                         ('Fortress Wasteland Gate Adult', 'Fortress Near Wasteland Adult'),
                         ('Fortress Near Wasteland to Bottom', 'Gerudo Fortress Adult'),
                         ('Fortress Upper Area Adult', 'Fortress Upper Area Adult'),
                         ('Fortress Middle to Bottom Adult', 'Gerudo Fortress Adult'),
                         ('Fortress L to Skulltula Adult', 'Fortress Rooftop Skulltula Adult'),
                         ('Fortress L to Middle Adult', 'Fortress Middle Level Adult'),
                         ('Fortress M to Bottom Adult', 'Gerudo Fortress Adult'),
                         ('Fortress N to Jail Adult', 'Fortress Jail Adult'),
                         ('Fortress N to M Adult', 'Fortress Entrance M Ledge Adult'),
                         ('Fortress N to Rooftop Chest Adult', 'Fortress Rooftop Chest Adult'),
                         ('Fortress Rooftop to Skulltula Adult', 'Fortress Rooftop Skulltula Adult'),
                         ('Fortress Rooftop to Rooftop Chest Adult', 'Fortress Rooftop Chest Adult'),
                         ('Fortress Rooftop to L Adult', 'Fortress Entrance L Ledge Adult'),
                         ('Fortress Rooftop Chest to Rooftops Adult', 'Fortress Rooftops Adult'),
                         ('Fortress Rooftop Chest to M Adult', 'Fortress Entrance M Ledge Adult'),
                         ('Fortress Jail to M Adult', 'Fortress Entrance M Ledge Adult'),
                         ('Fortress Upper Area to Bottom', 'Gerudo Fortress Adult'),
                         ('Fortress Entry from GTG to Bottom', 'Gerudo Fortress Adult'),
                         ('Hideout North F1 Final Rescue Adult', 'Hideout Final Rescue Adult'),
                         ('Hideout South F2 Final Rescue Adult', 'Hideout Final Rescue Adult'),
                         ('Hideout North F1 Final Rescue Adult', 'Hideout Final Rescue Adult'),
                         ('Hideout South F2 Final Rescue Adult', 'Hideout Final Rescue Adult'),
                         ('Hideout North F1 Savewarp Adult', 'Hideout North F1 Adult'),     # I decided that I don't want savewarps to be shuffled, but that could be changed.
                         ('Hideout North F2 Savewarp Adult', 'Hideout North F1 Adult'),
                         ('Hideout South F1 Savewarp Adult', 'Hideout North F1 Adult'),
                         ('Hideout South F2 Savewarp Adult', 'Hideout North F1 Adult'),
                         ('Hideout Kitchen Lower Savewarp Adult', 'Hideout North F1 Adult'),
                         ('Hideout Kitchen Upper West Savewarp Adult', 'Hideout North F1 Adult'),
                         ('Hideout Kitchen Upper East Savewarp Adult', 'Hideout North F1 Adult'),
                         ('Hideout Hallway Lower Savewarp Adult', 'Hideout North F1 Adult'),
                         ('Hideout Hallway Upper Savewarp Adult', 'Hideout North F1 Adult'),
                         ('Hideout Kitchen Lower to Upper West Adult', 'Hideout Kitchen Upper West Adult'),
                         ('Hideout Kitchen Lower to Upper East Adult', 'Hideout Kitchen Upper East Adult'),
                         ('Hideout Kitchen Upper West to Lower Adult', 'Hideout Kitchen Lower Adult'),
                         ('Hideout Kitchen Upper East to Lower Adult', 'Hideout Kitchen Lower Adult'),
                         ('Hideout Kitchen Upper West to East Adult', 'Hideout Kitchen Upper East Adult'),
                         ('Hideout Kitchen Upper East to West Adult', 'Hideout Kitchen Upper West Adult'),
                         ('Hideout Hallway Lower to Upper Adult', 'Hideout Hallway Upper Adult'),
                         ('Hideout Hallway Upper to Lower Adult', 'Hideout Hallway Lower Adult'),
                         ('Haunted Wasteland Sand River Adult', 'Haunted Wasteland Middle Adult'),
                         ('Haunted Wasteland Poe Guide Adult', 'Haunted Wasteland End Adult'),
                         ('Colossus From Spirit Child', 'Desert Colossus Child'),
                         ('Colossus From Spirit Adult', 'Desert Colossus Adult'),
                         ('Desert Colossus Song Child to Shared', 'Desert Colossus Song Shared'),
                         ('Desert Colossus Song Adult to Shared', 'Desert Colossus Song Shared'),
                         ('Colossus Fairy Child to Shared', 'Colossus Fairy Shared'),
                         ('Colossus Fairy Adult to Shared', 'Colossus Fairy Shared'),
                         ('Desert Colossus Right Hand Child to Shared', 'Desert Colossus Right Hand Shared'),
                         ('Desert Colossus Right Hand Adult to Shared', 'Desert Colossus Right Hand Shared'),
                         ('Colossus Right Hand Jump Down Child', 'Desert Colossus Child'),
                         ('Colossus Right Hand Jump Down Adult', 'Desert Colossus Adult'),
#                        ('Colossus Left Hand Jump Down Child', 'Desert Colossus Child'),
                         ('Colossus Left Hand Jump Down Adult', 'Desert Colossus Adult'),
#                        Right to Left Adult?
                         ('Desert Colossus Longshot Left to Right Adult', 'Desert Colossus Right Hand Adult'),
                         ('Kakariko Village Adult', 'Kakariko Village Adult'),
                         ('Kakariko Village Child to Shared', 'Kakariko Village Shared'),
                         ('Kakariko Village Adult to Shared', 'Kakariko Village Shared'),
                         ('House of Skulltulla Child to Shared', 'House of Skulltulla Shared'),
                         ('House of Skulltulla Adult to Shared', 'House of Skulltulla Shared'),
                         ('Impas House Back Child to Shared', 'Impas House Back Shared'),
                         ('Impas House Back Adult to Shared', 'Impas House Back Shared'),
                         ('Dampes Grave to Windmill Adult', 'Windmill Adult'),
                         ('Windmill Child to Shared', 'Windmill Shared'),
                         ('Windmill Adult to Shared', 'Windmill Shared'),
                         ('Dampe to Windmill Adult to Shared', 'Windmill Shared'),
                         ('Kakariko Bombable Grotto Child to Shared', 'Kakariko Bombable Grotto Shared'),
                         ('Kakariko Bombable Grotto Adult to Shared', 'Kakariko Bombable Grotto Shared'),
                         ('Kakariko Back Grotto Child to Shared', 'Kakariko Back Grotto Shared'),
                         ('Kakariko Back Grotto Adult to Shared', 'Kakariko Back Grotto Shared'),
                         ('Drop to Graveyard Child', 'Graveyard Child'),
                         ('Drop to Graveyard Adult', 'Graveyard Adult'),
                         ('Fairy Fountain Grave Child to Shared', 'Fairy Fountain Grave Shared'),
                         ('Fairy Fountain Grave Adult to Shared', 'Fairy Fountain Grave Shared'),
                         ('Redead Grave Child to Shared', 'Redead Grave Shared'),
                         ('Redead Grave Adult to Shared', 'Redead Grave Shared'),
                         ('Royal Family Tomb Chest Child to Shared', 'Royal Family Tomb Chest Shared'),
                         ('Royal Family Tomb Chest Adult to Shared', 'Royal Family Tomb Chest Shared'),
                         ('Royal Family Tomb Song Child to Shared', 'Royal Family Tomb Song Shared'),
                         ('Royal Family Tomb Song Adult to Shared', 'Royal Family Tomb Song Shared'),
                         ('Mountain Ascent Child', 'Death Mountain Trail Upper Child'),
                         ('Mountain Ascent Adult', 'Death Mountain Trail Upper Adult'),
                         ('Mountain Descent Child', 'Death Mountain Trail Child'),
                         ('Mountain Descent Adult', 'Death Mountain Trail Adult'),
                         ('Death Mountain Trail Bomb Wall Child to Shared', 'Death Mountain Trail Bomb Wall Shared'),
                         ('Death Mountain Trail Bomb Wall Adult to Shared', 'Death Mountain Trail Bomb Wall Shared'),
                         ('Death Mountain Trail PoH Child to Shared', 'Death Mountain Trail PoH Shared'),
                         ('Death Mountain Trail PoH Adult to Shared', 'Death Mountain Trail PoH Shared'),
                         ('Mountain Storms Grotto Child to Shared', 'Mountain Storms Grotto Shared'),
                         ('Mountain Storms Grotto Adult to Shared', 'Mountain Storms Grotto Shared'),
                         ('Mountain Fairy Child to Shared', 'Mountain Fairy Shared'),
                         ('Mountain Fairy Adult to Shared', 'Mountain Fairy Shared'),
                         ('Goron City Out Through Rocks Child', 'Goron City Lost Woods Rocks Child'),
                         ('Goron City Out Through Rocks Adult', 'Goron City Lost Woods Rocks Adult'),
                         ('Goron City In Through Rocks Child', 'Goron City Child'),
                         ('Goron City In Through Rocks Adult', 'Goron City Adult'),
                         ('Goron City Darunia Child', 'Goron City Darunia Child'),
                         ('Goron City Darunia Adult', 'Goron City Darunia Adult'),
                         ('Goron City Lava Adult', 'Goron City Lava Adult'),
#                        ('Goron City Lava Reverse Child', 'Goron City Child'),
                         ('Goron City Lava Reverse Adult', 'Goron City Adult'),
                         ('Goron City Child to Shared', 'Goron City Shared'),
                         ('Goron City Adult to Shared', 'Goron City Shared'),
                         ('Crater Hover Boots to Lower Adult', 'Death Mountain Crater Lower Adult'),
                         ('Crater Scarecrow to Central Adult', 'Death Mountain Crater Central Adult'),
#                        ('Crater Ascent to Upper Child', 'Death Mountain Crater Upper Child'),
                         ('Crater Ascent to Upper Adult', 'Death Mountain Crater Upper Adult'),
                         ('Crater Bridge to Central Adult', 'Death Mountain Crater Central Adult'),
                         ('Crater Bridge Reverse to Lower Adult', 'Death Mountain Crater Lower Adult'),
                         ('Death Mountain Crater Child to Shared', 'Death Mountain Crater Shared'),
                         ('Death Mountain Crater Adult to Shared', 'Death Mountain Crater Shared'),
                         ('Hyrule Castle Upper Child', 'Hyrule Castle Upper Child'),
                         ('Door of Time', 'Beyond Door of Time'),
                         ('To Adult', 'Temple of Time Adult'),
                         ('To Child', 'Temple of Time Child'),

                         ('Deku Tree Slingshot Passage', 'Deku Tree Slingshot Room'),
                         ('Deku Tree Slingshot Exit', 'Deku Tree Child'),
                         ('Deku Tree Basement Path', 'Deku Tree Boss Room'),
                         ('Deku Tree Basement Vines', 'Deku Tree Child'),
                         ('Dodongos Cavern Lobby Child', 'Dodongos Cavern Lobby Child'),
                         ('Dodongos Cavern Lobby Adult', 'Dodongos Cavern Lobby Adult'),
                         ('Dodongos Cavern Retreat Child', 'Dodongos Cavern Child'),
                         ('Dodongos Cavern Retreat Adult', 'Dodongos Cavern Adult'),
                         ('Dodongos Cavern Lobby Child to Shared', 'Dodongos Cavern Lobby Shared'),
                         ('Dodongos Cavern Lobby Adult to Shared', 'Dodongos Cavern Lobby Shared'),
                         ('Dodongos Cavern Left Door Child', 'Dodongos Cavern Climb Child'),
                         ('Dodongos Cavern Left Door Adult', 'Dodongos Cavern Climb Adult'),
                         ('Dodongos Cavern Slingshot Target Child', 'Dodongos Cavern Far Bridge Child'),
                         ('Dodongos Cavern Slingshot Target Adult', 'Dodongos Cavern Far Bridge Adult'),
                         ('Dodongos Cavern Climb Child to Shared', 'Dodongos Cavern Climb Shared'),
                         ('Dodongos Cavern Climb Adult to Shared', 'Dodongos Cavern Climb Shared'),
                         ('Dodongos Cavern Bomb Bag Child to Shared', 'Dodongos Cavern Bomb Bag Shared'),
                         ('Dodongos Cavern Bomb Bag Adult to Shared', 'Dodongos Cavern Bomb Bag Shared'),
                         ('Dodongos Cavern End of Bridge Child to Shared', 'Dodongos Cavern End of Bridge Shared'),
                         ('Dodongos Cavern End of Bridge Adult to Shared', 'Dodongos Cavern End of Bridge Shared'),
                         ('Dodongos Cavern GS Above Stairs Child to Shared', 'Dodongos Cavern GS Above Stairs Shared'),
                         ('Dodongos Cavern GS Above Stairs Adult to Shared', 'Dodongos Cavern GS Above Stairs Shared'),
                         ('Dodongos Cavern Bomb Drop Child', 'Dodongos Cavern Boss Area Child'),
                         ('Dodongos Cavern Bomb Drop Adult', 'Dodongos Cavern Boss Area Adult'),
                         ('Dodongos Cavern Boss Area Child to Shared', 'Dodongos Cavern Boss Area Shared'),
                         ('Dodongos Cavern Boss Area Adult to Shared', 'Dodongos Cavern Boss Area Shared'),
                         ('Dodongos Cavern King Dodongo Child to Shared', 'Dodongos Cavern King Dodongo Shared'),
                         ('Dodongos Cavern King Dodongo Adult to Shared', 'Dodongos Cavern King Dodongo Shared'),
                         ('Jabu Jabus Belly Ceiling Switch', 'Jabu Jabus Belly Main'),
                         ('Jabu Jabus Belly Retreat', 'Jabu Jabus Belly Child'),
                         ('Jabu Jabus Belly Tentacles', 'Jabu Jabus Belly Depths'),
                         ('Jabu Jabus Belly Elevator', 'Jabu Jabus Belly Main'),
                         ('Jabu Jabus Belly Octopus', 'Jabu Jabus Belly Boss Area'),
                         ('Jabu Jabus Belly Final Backtrack', 'Jabu Jabus Belly Main'),
                         ('Forest Temple Song of Time Block', 'Forest Temple NW Outdoors'),
                         ('Forest Temple Lobby Eyeball Switch', 'Forest Temple NE Outdoors'),
                         ('Forest Temple Lobby Locked Door', 'Forest Temple Block Push Room'),
                         ('Forest Temple Through Map Room', 'Forest Temple NE Outdoors'),
                         ('Forest Temple Well Connection', 'Forest Temple NW Outdoors'),
                         ('Forest Temple Outside to Lobby', 'Forest Temple Adult'),
                         ('Forest Temple Scarecrows Song', 'Forest Temple Falling Room'),
                         ('Forest Temple Falling Room Exit', 'Forest Temple NE Outdoors'),
                         ('Forest Temple Elevator', 'Forest Temple Boss Region'),
                         ('Forest Temple Outside Backdoor', 'Forest Temple Outside Upper Ledge'),
                         ('Forest Temple Twisted Hall', 'Forest Temple Bow Region'),
                         ('Forest Temple Straightened Hall', 'Forest Temple Straightened Hall'),
                         ('Forest Temple Boss Key Chest Drop', 'Forest Temple Outside Upper Ledge'),
                         ('Forest Temple Outside Ledge Drop', 'Forest Temple NW Outdoors'),
                         ('Forest Temple Drop to Falling Room', 'Forest Temple Falling Room'),
                         ('Fire Temple Early Climb', 'Fire Temple Middle'),
                         ('Fire Temple Fire Maze Escape', 'Fire Temple Upper'),
                         ('Water Temple Central Pillar', 'Water Temple Middle Water Level'),
                         ('Water Temple Upper Locked Door', 'Water Temple Dark Link Region'),
                         ('Shadow Temple First Gap', 'Shadow Temple Early'),
                         ('Shadow Temple First Pit', 'Shadow Temple First Beamos'),
                         ('Shadow Temple Bomb Wall', 'Shadow Temple Huge Pit'),
                         ('Shadow Temple Hookshot Target', 'Shadow Temple Wind Tunnel'),
                         ('Shadow Temple Boat', 'Shadow Temple Beyond Boat'),
                         ('Spirit Silver Block Adult', 'Spirit Adult Lower Adult'),
                         ('Spirit Lower Child Locked Door Child', 'Spirit Child Middle Child'),
                         ('Spirit Lower Adult Locked Door Adult', 'Spirit Central Adult'),
                         ('Spirit Bomb for Light Child', 'Spirit Central Child'),
                         ('Spirit Middle Child Door Adult', 'Spirit Child Middle Adult'),
                         ('Spirit Upper Child Locked Door Child', 'Spirit Child Upper Child'),
                         ('Spirit Upper Child Locked Door Adult', 'Spirit Child Upper Adult'),
                         ('Spirit Central Locked Door Adult', 'Spirit Anubis Room Adult'),
                         ('Spirit Anubis Room Clear Adult', 'Spirit Adult Upper Adult'),
                         ('Spirit Final Locked Door Adult', 'Spirit Final Area Adult'),
                         ('Spirit Child Middle Chests Child to Shared', 'Spirit Child Middle Chests Shared'),
                         ('Spirit Child Middle Chests Adult to Shared', 'Spirit Child Middle Chests Shared'),
                         ('Spirit Child Middle GS Child to Shared', 'Spirit Child Middle GS Shared'),
                         ('Spirit Child Middle GS Adult to Shared', 'Spirit Child Middle GS Shared'),
                         ('Spirit Central Chests Child to Shared', 'Spirit Central Chests Shared'),
                         ('Spirit Central Chests Adult to Shared', 'Spirit Central Chests Shared'),
                         ('Spirit Central GS Child to Shared', 'Spirit Central GS Shared'),
                         ('Spirit Central GS Adult to Shared', 'Spirit Central GS Shared'),
                         ('Gerudo Training Ground Left Silver Rupees', 'Gerudo Training Grounds Heavy Block Room'),
                         ('Gerudo Training Ground Beamos', 'Gerudo Training Grounds Lava Room'),
                         ('Gerudo Training Ground Central Door', 'Gerudo Training Grounds Central Maze'),
                         ('Gerudo Training Grounds Right Locked Doors', 'Gerudo Training Grounds Central Maze Right'),
                         ('Gerudo Training Grounds Maze Exit', 'Gerudo Training Grounds Lava Room'),
                         ('Gerudo Training Grounds Maze Ledge', 'Gerudo Training Grounds Central Maze Right'),
                         ('Gerudo Training Grounds Right Hookshot Target', 'Gerudo Training Grounds Hammer Room'),
                         ('Gerudo Training Grounds Hammer Target', 'Gerudo Training Grounds Eye Statue Lower'),
                         ('Gerudo Training Grounds Hammer Room Clear', 'Gerudo Training Grounds Lava Room'),
                         ('Gerudo Training Grounds Eye Statue Exit', 'Gerudo Training Grounds Hammer Room'),
                         ('Gerudo Training Grounds Eye Statue Drop', 'Gerudo Training Grounds Eye Statue Lower'),
                         ('Gerudo Training Grounds Hidden Hookshot Target', 'Gerudo Training Grounds Eye Statue Upper'),
                         ('Ganons Castle Forest Trial', 'Ganons Castle Forest Trial'),
                         ('Ganons Castle Fire Trial', 'Ganons Castle Fire Trial'),
                         ('Ganons Castle Water Trial', 'Ganons Castle Water Trial'),
                         ('Ganons Castle Shadow Trial', 'Ganons Castle Shadow Trial'),
                         ('Ganons Castle Spirit Trial', 'Ganons Castle Spirit Trial'),
                         ('Ganons Castle Light Trial', 'Ganons Castle Light Trial'),
                         ('Ganons Castle Tower', 'Ganons Castle Tower')
                        ]

# non-shuffled entrance links
default_connections = [('Minuet of Forest Child', 'Sacred Forest Meadow Child'),
                       ('Minuet of Forest Adult', 'Sacred Forest Meadow Adult'),
                       ('Bolero of Fire Child', 'Death Mountain Crater Central Child'),
                       ('Bolero of Fire Adult', 'Death Mountain Crater Central Adult'),
                       ('Serenade of Water Child', 'Lake Hylia Child'),
                       ('Serenade of Water Adult', 'Lake Hylia Adult'),
                       ('Nocturne of Shadow Child', 'Shadow Temple Warp Child'),
                       ('Nocturne of Shadow Adult', 'Shadow Temple Warp Adult'),
                       ('Requiem of Spirit Child', 'Desert Colossus Child'),
                       ('Requiem of Spirit Adult', 'Desert Colossus Adult'),
                       ('Prelude of Light Child', 'Temple of Time Child'),
                       ('Prelude of Light Adult', 'Temple of Time Adult'),
                       ('Links House Child', 'Links House Child'),
                       ('Links House Adult', 'Links House Adult'),
                       ('Links House Exit Child', 'Kokiri Forest Child'),
                       ('Links House Exit Adult', 'Kokiri Forest Adult'),
                       ('Mido House Child', 'Mido House Child'),
                       ('Mido House Adult', 'Mido House Adult'),
                       ('Mido House Exit Child', 'Kokiri Forest Child'),
                       ('Mido House Exit Adult', 'Kokiri Forest Adult'),
                       ('Saria House Child', 'Saria House Child'),
                       ('Saria House Adult', 'Saria House Adult'),
                       ('Saria House Exit Child', 'Kokiri Forest Child'),
                       ('Saria House Exit Adult', 'Kokiri Forest Adult'),
                       ('House of Twins Child', 'House of Twins Child'),
                       ('House of Twins Adult', 'House of Twins Adult'),
                       ('House of Twins Exit Child', 'Kokiri Forest Child'),
                       ('House of Twins Exit Adult', 'Kokiri Forest Adult'),
                       ('Know It All House Child', 'Know It All House Child'),
                       ('Know It All House Adult', 'Know It All House Adult'),
                       ('Know It All House Exit Child', 'Kokiri Forest Child'),
                       ('Know It All House Exit Adult', 'Kokiri Forest Adult'),
                       ('Kokiri Shop Child', 'Kokiri Shop Child'),
                       ('Kokiri Shop Adult', 'Kokiri Shop Adult'),
                       ('Kokiri Shop Exit Child', 'Kokiri Forest Child'),
                       ('Kokiri Shop Exit Adult', 'Kokiri Forest Adult'),
                       ('Kokiri Forest Storms Grotto Child', 'Kokiri Forest Storms Grotto Child'),
                       ('Kokiri Forest Storms Grotto Adult', 'Kokiri Forest Storms Grotto Adult'),
                       ('Kokiri Forest Storms Grotto Exit Child', 'Kokiri Forest Child'),
                       ('Kokiri Forest Storms Grotto Exit Adult', 'Kokiri Forest Adult'),
                       ('Lost Woods Ocarina Child', 'Lost Woods Ocarina Child'),
                       ('Lost Woods Ocarina Adult', 'Lost Woods Ocarina Adult'),
                       ('Kokiri Forest Entrance Child', 'Kokiri Forest Child'),
                       ('Kokiri Forest Entrance Adult', 'Kokiri Forest Adult'),
                       ('Forest Exit Child', 'Hyrule Field Child'),
                       ('Forest Exit Adult', 'Hyrule Field Adult'),
                       ('Lost Woods Child', 'Lost Woods Child'),
                       ('Lost Woods Adult', 'Lost Woods Adult'),
                       ('Lost Woods to Kokiri Forest Child', 'Kokiri Forest Child'),
                       ('Lost Woods to Kokiri Forest Adult', 'Kokiri Forest Adult'),
                       ('Lost Woods Get Lost Adult', 'Kokiri Forest Adult'), # same loading zone as previous two
                       ('Lost Woods Generic Grotto Child', 'Lost Woods Generic Grotto Child'),
                       ('Lost Woods Generic Grotto Adult', 'Lost Woods Generic Grotto Adult'),
                       ('Lost Woods Generic Grotto Exit Child', 'Lost Woods Child'),
                       ('Lost Woods Generic Grotto Exit Adult', 'Lost Woods Adult'),
                       ('Deku Theater Grotto Child', 'Deku Theater Grotto Child'),
                       ('Deku Theater Grotto Adult', 'Deku Theater Grotto Adult'),
                       ('Deku Theater Grotto Exit Child', 'Lost Woods Child'),
                       ('Deku Theater Grotto Exit Adult', 'Lost Woods Past Mido Adult'),
                       ('Lost Woods Sales Grotto Child', 'Lost Woods Sales Grotto Child'),
                       ('Lost Woods Sales Grotto Adult', 'Lost Woods Sales Grotto Adult'),
                       ('Lost Woods Sales Grotto Exit Child', 'Lost Woods Child'),
                       ('Lost Woods Sales Grotto Exit Adult', 'Lost Woods Past Mido Adult'),
                       ('Lost Woods to Goron City Child', 'Goron City Lost Woods Rocks Child'),
                       ('Lost Woods to Goron City Adult', 'Goron City Lost Woods Rocks Adult'),
                       ('Lost Woods to Zora River Child', 'Zora River Top Child'),
                       ('Lost Woods to Zora River Adult', 'Zora River Adult'),
                       ('Sacred Forest Meadow Child', 'Sacred Forest Meadow Child'),
                       ('Sacred Forest Meadow Adult', 'Sacred Forest Meadow Adult'),
                       ('Sacred Forest Meadow Exit Child', 'Lost Woods Child'),
                       ('Sacred Forest Meadow Exit Adult', 'Lost Woods Past Mido Adult'),
                       ('Meadow Wolfos Grotto Child', 'Meadow Wolfos Grotto Child'),
                       ('Meadow Wolfos Grotto Adult', 'Meadow Wolfos Grotto Adult'),
                       ('Meadow Wolfos Grotto Exit Child', 'Sacred Forest Meadow Child'),
                       ('Meadow Wolfos Grotto Exit Adult', 'Sacred Forest Meadow Adult'),
                       ('Meadow Fairy Grotto Child', 'Meadow Fairy Grotto Child'),
                       ('Meadow Fairy Grotto Adult', 'Meadow Fairy Grotto Adult'),
                       ('Meadow Fairy Grotto Exit Child', 'Sacred Forest Meadow Child'),
                       ('Meadow Fairy Grotto Exit Adult', 'Sacred Forest Meadow Adult'),
                       ('Meadow Storms Grotto Child', 'Meadow Storms Grotto Child'),
                       ('Meadow Storms Grotto Adult', 'Meadow Storms Grotto Adult'),
                       ('Meadow Storms Grotto Exit Child', 'Sacred Forest Meadow Child'),
                       ('Meadow Storms Grotto Exit Adult', 'Sacred Forest Meadow Adult'),
                       ('Hyrule Field to Lost Woods Child', 'Lost Woods Bridge Child'),
                       ('Hyrule Field to Lost Woods Adult', 'Lost Woods Bridge Adult'),
                       ('Remote Southern Grotto Child', 'Remote Southern Grotto Child'),
                       ('Remote Southern Grotto Adult', 'Remote Southern Grotto Adult'),
                       ('Remote Southern Grotto Exit Child', 'Hyrule Field Child'),
                       ('Remote Southern Grotto Exit Adult', 'Hyrule Field Adult'),
                       ('Field Near Lake Outside Fence Grotto Child', 'Field Near Lake Outside Fence Grotto Child'),
                       ('Field Near Lake Outside Fence Grotto Adult', 'Field Near Lake Outside Fence Grotto Adult'),
                       ('Field Near Lake Outside Fence Grotto Exit Child', 'Hyrule Field Child'),
                       ('Field Near Lake Outside Fence Grotto Exit Adult', 'Hyrule Field Adult'),
                       ('Field Near Lake Inside Fence Grotto Child', 'Field Near Lake Inside Fence Grotto Child'),
                       ('Field Near Lake Inside Fence Grotto Adult', 'Field Near Lake Inside Fence Grotto Adult'),
                       ('Field Near Lake Inside Fence Grotto Exit Child', 'Hyrule Field Child'),
                       ('Field Near Lake Inside Fence Grotto Exit Adult', 'Hyrule Field Adult'),
                       ('Field Near Valley Grotto Child', 'Field Near Valley Grotto Child'),
                       ('Field Near Valley Grotto Adult', 'Field Near Valley Grotto Adult'),
                       ('Field Near Valley Grotto Exit Child', 'Hyrule Field Child'),
                       ('Field Near Valley Grotto Exit Adult', 'Hyrule Field Adult'),
                       ('Field West Castle Town Grotto Child', 'Field West Castle Town Grotto Child'),
                       ('Field West Castle Town Grotto Adult', 'Field West Castle Town Grotto Adult'),
                       ('Field West Castle Town Grotto Exit Child', 'Hyrule Field Child'),
                       ('Field West Castle Town Grotto Exit Adult', 'Hyrule Field Adult'),
                       ('Field Far West Castle Town Grotto Child', 'Field Far West Castle Town Grotto Child'),
                       ('Field Far West Castle Town Grotto Adult', 'Field Far West Castle Town Grotto Adult'),
                       ('Field Far West Castle Town Grotto Exit Child', 'Hyrule Field Child'),
                       ('Field Far West Castle Town Grotto Exit Adult', 'Hyrule Field Adult'),
                       ('Field Near Kakariko Grotto Child', 'Field Near Kakariko Grotto Child'),
                       ('Field Near Kakariko Grotto Adult', 'Field Near Kakariko Grotto Adult'),
                       ('Field Near Kakariko Grotto Exit Child', 'Hyrule Field Child'),
                       ('Field Near Kakariko Grotto Exit Adult', 'Hyrule Field Adult'),
                       ('Field North of Lon Lon Grotto Child', 'Field North of Lon Lon Grotto Child'),
                       ('Field North of Lon Lon Grotto Adult', 'Field North of Lon Lon Grotto Adult'),
                       ('Field North of Lon Lon Grotto Exit Child', 'Hyrule Field Child'),
                       ('Field North of Lon Lon Grotto Exit Adult', 'Hyrule Field Adult'),
                       ('Lake Hylia Child', 'Lake Hylia Child'),
                       ('Lake Hylia Adult', 'Lake Hylia Adult'),
                       ('Gerudo Valley Child', 'Gerudo Valley Child'),
                       ('Gerudo Valley Adult', 'Gerudo Valley Adult'),
                       ('Market Entrance Child', 'Market Entrance Child'),
                       ('Market Entrance Adult', 'Market Entrance Adult'),
                       ('Kakariko Village Child', 'Kakariko Village Child'),
                       ('Kakariko Village Song', 'Kakariko Village Song'), # Adult version of previous entrance
                       ('Zora River Land Child', 'Zora River Bottom Child'),
                       ('Zora River Land Adult', 'Zora River Adult'),
                       ('Zora River Water Child', 'Zora River Bottom Child'),
                       ('Zora River Water Adult', 'Zora River Adult'),
                       ('Lon Lon Ranch Child', 'Lon Lon Ranch Child'),
                       ('Lon Lon Ranch Adult', 'Lon Lon Ranch Adult'),
                       ('Lon Lon Exit Child', 'Hyrule Field Child'),
                       ('Lon Lon Exit Adult', 'Hyrule Field Adult'),
                       ('Talon House Child', 'Talon House Child'),
                       ('Talon House Adult', 'Talon House Adult'),
                       ('Talon House Exit Child', 'Lon Lon Ranch Child'),
                       ('Talon House Exit Adult', 'Lon Lon Ranch Adult'),
                       ('Ingo Barn Child', 'Ingo Barn Child'),
                       ('Ingo Barn Adult', 'Ingo Barn Adult'),
                       ('Ingo Barn Exit Child', 'Lon Lon Ranch Child'),
                       ('Ingo Barn Exit Adult', 'Lon Lon Ranch Adult'),
                       ('Lon Lon Corner Tower Child', 'Lon Lon Corner Tower Child'),
                       ('Lon Lon Corner Tower Adult', 'Lon Lon Corner Tower Adult'),
                       ('Lon Lon Corner Tower Exit Child', 'Lon Lon Ranch Child'),
                       ('Lon Lon Corner Tower Exit Adult', 'Lon Lon Ranch Adult'),
                       ('Lon Lon Grotto Child', 'Lon Lon Grotto Child'),
                       ('Lon Lon Grotto Exit Child', 'Lon Lon Ranch Child'),
#                      Lon Lon Grotto Adult?
#                      Child Epona Gates?
                       ('Epona East Gate Adult', 'Hyrule Field Adult'),
#                      Child Epona Gates?
                       ('Epona West Gate Adult', 'Hyrule Field Adult'),
#                      Child Epona Gates?
                       ('Epona South Gate Adult', 'Hyrule Field Adult'),
                       ('Zora River Land Exit Child', 'Hyrule Field Child'),
                       ('Zora River Land Exit Adult', 'Hyrule Field Adult'),
                       ('Zora River Water Exit Child', 'Hyrule Field Child'),
                       ('Zora River Water Exit Adult', 'Hyrule Field Adult'),
                       ('Zora River to Lost Woods Child', 'Lost Woods Child'),
                       ('Zora River to Lost Woods Adult', 'Lost Woods Adult'),
                       ('Zora River Storms Grotto Child', 'Zora River Storms Grotto Child'),
                       ('Zora River Storms Grotto Adult', 'Zora River Storms Grotto Adult'),
                       ('Zora River Storms Grotto Exit Child', 'Zora River Top Child'),
                       ('Zora River Storms Grotto Exit Adult', 'Zora River Adult'),
                       ('Zora River Plateau Open Grotto Child', 'Zora River Plateau Open Grotto Child'),
                       ('Zora River Plateau Open Grotto Adult', 'Zora River Plateau Open Grotto Adult'),
                       ('Zora River Plateau Open Grotto Exit Child', 'Zora River Top Child'),
                       ('Zora River Plateau Open Grotto Exit Adult', 'Zora River Adult'),
                       ('Zora River Plateau Bombable Grotto Child', 'Zora River Plateau Bombable Grotto Child'),
                       ('Zora River Plateau Bombable Grotto Adult', 'Zora River Plateau Bombable Grotto Adult'),
                       ('Zora River Plateau Bombable Grotto Exit Child', 'Zora River Top Child'),
                       ('Zora River Plateau Bombable Grotto Exit Adult', 'Zora River Adult'),
                       ('Zoras Domain Child', 'Zoras Domain Child'),
                       ('Zoras Domain Adult', 'Zoras Domain Adult'),
                       ('Zoras Domain Exit Child', 'Zora River Top Child'),
                       ('Zoras Domain Exit Adult', 'Zora River Adult'),
                       ('Zora Shop Child', 'Zora Shop Child'),
                       ('Zora Shop Adult', 'Zora Shop Adult'),
                       ('Zora Shop Exit Child', 'Zoras Domain Child'),
                       ('Zora Shop Exit Adult', 'Zoras Domain Adult'),
                       ('Zoras Domain Storms Grotto Child', 'Zoras Domain Storms Grotto Child'),
                       ('Zoras Domain Storms Grotto Adult', 'Zoras Domain Storms Grotto Adult'),
                       ('Zoras Domain Storms Grotto Exit Child', 'Zoras Domain Child'),
                       ('Zoras Domain Storms Grotto Exit Adult', 'Zoras Domain Adult'),
                       ('Zoras Domain to Lake Hylia Child', 'Lake Hylia Child'),
#                      Adult Dive Warp
                       ('Zoras Fountain Child', 'Zoras Fountain Child'),
                       ('Zoras Fountain Adult', 'Zoras Fountain Adult'),
                       ('Zoras Fountain Exit Child', 'Zoras Domain Child'),
                       ('Zoras Fountain Exit Adult', 'Zoras Domain Adult'),
                       ('Zoras Fountain Fairy Child', 'Zoras Fountain Fairy Child'),
                       ('Zoras Fountain Fairy Adult', 'Zoras Fountain Fairy Adult'),
                       ('Zoras Fountain Fairy Exit Child', 'Zoras Fountain Child'),
                       ('Zoras Fountain Fairy Exit Adult', 'Zoras Fountain Adult'),
                       ('Lake Hylia Exit Child', 'Hyrule Field Child'),
                       ('Lake Hylia Exit Adult', 'Hyrule Field Adult'),
                       ('Lake Hylia to Zoras Domain Child', 'Zoras Domain Child'),
#                      Adult Dive Warp?
                       ('Lake Hylia Lab Child', 'Lake Hylia Lab Child'),
                       ('Lake Hylia Lab Adult', 'Lake Hylia Lab Adult'),
                       ('Lake Hylia Lab Exit Child', 'Lake Hylia Child'),
                       ('Lake Hylia Lab Exit Adult', 'Lake Hylia Adult'),
                       ('Lake Hylia Owl Child', 'Hyrule Field Child'),
#                      Adult Owl?
                       ('Fishing Hole Child', 'Fishing Hole Child'),
                       ('Fishing Hole Adult', 'Fishing Hole Adult'),
                       ('Fishing Hole Exit Child', 'Lake Hylia Child'),
                       ('Fishing Hole Exit Adult', 'Lake Hylia Adult'),
                       ('Lake Hylia Grotto Child', 'Lake Hylia Grotto Child'),
                       ('Lake Hylia Grotto Adult', 'Lake Hylia Grotto Adult'),
                       ('Lake Hylia Grotto Exit Child', 'Lake Hylia Child'),
                       ('Lake Hylia Grotto Exit Adult', 'Lake Hylia Adult'),
                       ('Gerudo Valley Exit Child', 'Hyrule Field Child'),
                       ('Gerudo Valley Exit Adult', 'Hyrule Field Adult'),
                       ('Gerudo Valley River Child', 'Lake Hylia Child'),
                       ('Gerudo Valley River Adult', 'Lake Hylia Adult'),
#                      ('Gerudo Valley Silver Rock River Child', 'Lake Hylia Child'), # same loading zone as previous two
                       ('Gerudo Valley Silver Rock River Adult', 'Lake Hylia Adult'), # same loading zone as previous three
#                      Child Tent?
                       ('Gerudo Valley Tent Adult', 'Gerudo Valley Tent Adult'),
#                      Child Tent?
                       ('Gerudo Valley Tent Exit Adult', 'Gerudo Valley Far Side Adult'),
#                      Child Storms Grotto?
                       ('Gerudo Valley Storms Grotto Adult', 'Gerudo Valley Storms Grotto Adult'),
#                      Child Storms Grotto?
                       ('Gerudo Valley Storms Grotto Exit Adult', 'Gerudo Valley Far Side Adult'),
#                      Child Silver Rock Grotto?
                       ('Gerudo Valley Silver Rock Grotto Adult', 'Gerudo Valley Silver Rock Grotto Adult'),
#                      Child Silver Rock Grotto?
                       ('Gerudo Valley Silver Rock Grotto Exit Adult', 'Gerudo Valley Silver Rock Adult'),
#                      Child Gerudo Fortress?
                       ('Gerudo Fortress Adult', 'Gerudo Fortress Adult'),
#                      Child Gerudo Fortress?
                       ('Gerudo Fortress Exit Adult', 'Gerudo Valley Far Side Adult'),
#                      Child Fortress Storms Grotto?
                       ('Fortress Storms Grotto Adult', 'Gerudo Fortress Adult'),
#                      Child Fortress Storms Grotto?
                       ('Fortress Storms Grotto Exit Adult', 'Gerudo Fortress Adult'),
#                      Child Fortress Guard?
#                      Adult Fortress Guard?
#                      Child Hideout?
                       ('Thieves Hideout B Adult', 'Hideout North F1 Adult'),
#                      Child Hideout?
                       ('Hideout B Exit Adult', 'Gerudo Fortress Adult'),
#                      Child Hideout?
                       ('Thieves Hideout C Adult', 'Hideout North F1 Adult'),
#                      Child Hideout?
                       ('Hideout C Exit Adult', 'Gerudo Fortress Adult'),
#                      Child Hideout?
                       ('Thieves Hideout D Adult', 'Hideout Kitchen Lower Adult'),
#                      Child Hideout?
                       ('Hideout D Exit Adult', 'Gerudo Fortress Adult'),
#                      Child Hideout?
                       ('Thieves Hideout E Adult', 'Hideout Kitchen Lower Adult'),
#                      Child Hideout?
                       ('Hideout E Exit Adult', 'Gerudo Fortress Adult'),
#                      Child Hideout?
                       ('Thieves Hideout F Adult', 'Hideout Kitchen Upper West Adult'),
#                      Child Hideout?
                       ('Hideout F Exit Adult', 'Fortress Middle Level Adult'),
#                      Child Hideout?
                       ('Thieves Hideout G Adult', 'Hideout Kitchen Upper East Adult'),
#                      Child Hideout?
                       ('Hideout G Exit Adult', 'Fortress Rooftops Adult'),
#                      Child Hideout?
                       ('Thieves Hideout H Adult', 'Hideout South F2 Adult'),
#                      Child Hideout?
                       ('Hideout H Exit Adult', 'Gerudo Fortress Adult'),
#                      Child Hideout?
                       ('Thieves Hideout I Adult', 'Hideout South F2 Adult'),
#                      Child Hideout?
                       ('Hideout I Exit Adult', 'Fortress Middle Level Adult'),
#                      Child Hideout?
                       ('Thieves Hideout J Adult', 'Hideout South F1 Adult'),
#                      Child Hideout?
                       ('Hideout J Exit Adult', 'Fortress Middle Level Adult'),
#                      Child Hideout?
                       ('Thieves Hideout K Adult', 'Hideout South F1 Adult'),
#                      Child Hideout?
                       ('Hideout K Exit Adult', 'Gerudo Fortress Adult'),
#                      Child Hideout?
                       ('Thieves Hideout L Adult', 'Hideout North F2 Adult'),
#                      Child Hideout?
                       ('Hideout L Exit Adult', 'Fortress Entrance L Ledge Adult'),
#                      Child Hideout?
                       ('Thieves Hideout M Adult', 'Hideout Hallway Lower Adult'),
#                      Child Hideout?
                       ('Hideout M Exit Adult', 'Fortress Entrance M Ledge Adult'),
#                      Child Hideout?
                       ('Thieves Hideout N Adult', 'Hideout Hallway Upper Adult'),
#                      Child Hideout?
                       ('Hideout N Exit Adult', 'Fortress Entrance N Ledge Adult'),
#                      Child Fortress?
                       ('Haunted Wasteland Adult', 'Haunted Wasteland Start Adult'),
#                      Child Wasteland?
                       ('Haunted Wasteland Exit Adult', 'Fortress Near Wasteland Adult'),
                       ('Desert Colossus Child', 'Desert Colossus Child'),
                       ('Desert Colossus Adult', 'Desert Colossus Adult'),
                       ('Desert Colossus Exit Child', 'Haunted Wasteland End Child'),
                       ('Desert Colossus Exit Adult', 'Haunted Wasteland End Adult'),
                       ('Colossus Fairy Child', 'Colossus Fairy Child'),
                       ('Colossus Fairy Adult', 'Colossus Fairy Adult'),
                       ('Colossus Fairy Exit Child', 'Desert Colossus Child'),
                       ('Colossus Fairy Exit Adult', 'Desert Colossus Adult'),
#                      ('Colossus Silver Rock Grotto Child', 'Colossus Silver Rock Grotto Child'),
                       ('Colossus Silver Rock Grotto Adult', 'Colossus Silver Rock Grotto Adult'),
#                      ('Colossus Silver Rock Grotto Exit Child', 'Desert Colossus Child'),
                       ('Colossus Silver Rock Grotto Exit Adult', 'Desert Colossus Adult'),
                       ('Kakariko Village Exit Child', 'Hyrule Field Child'),
                       ('Kakariko Village Exit Adult', 'Hyrule Field Adult'),
                       ('Carpenter Boss House Child', 'Carpenter Boss House Child'),
                       ('Carpenter Boss House Adult', 'Carpenter Boss House Adult'),
                       ('Carpenter Boss House Exit Child', 'Kakariko Village Child'),
                       ('Carpenter Boss House Exit Adult', 'Kakariko Village Adult'),
                       ('House of Skulltulla Child', 'House of Skulltulla Child'),
                       ('House of Skulltulla Adult', 'House of Skulltulla Adult'),
                       ('House of Skulltulla Exit Child', 'Kakariko Village Child'),
                       ('House of Skulltulla Exit Adult', 'Kakariko Village Adult'),
                       ('Impas House Child', 'Impas House Child'),
                       ('Impas House Adult', 'Impas House Adult'),
                       ('Impas House Exit Child', 'Kakariko Village Child'),
                       ('Impas House Exit Adult', 'Kakariko Village Adult'),
                       ('Impas House Back Child', 'Impas House Back Child'),
                       ('Impas House Back Adult', 'Impas House Back Adult'),
                       ('Impas House Back Exit Child', 'Kakariko Village Child'),
                       ('Impas House Back Exit Adult', 'Kakariko Village Adult'),
                       ('Windmill Child', 'Windmill Child'),
                       ('Windmill Adult', 'Windmill Adult'),
                       ('Windmill Exit Child', 'Kakariko Village Child'),
                       ('Windmill Exit Adult', 'Kakariko Village Adult'),
#                      Child Dampes Grave?
                       ('Dampes Grave Adult', 'Dampes Grave Adult'),
#                      Child Dampes Grave?
                       ('Dampes Grave Exit Adult', 'Graveyard Adult'),
#                      Child Kakariko Bazaar?
                       ('Kakariko Bazaar Adult', 'Kakariko Bazaar Adult'),
#                      Child Kakariko Bazaar?
                       ('Kakariko Bazaar Exit Adult', 'Kakariko Village Adult'),
#                      Child Kakariko Shooting Gallery?
                       ('Kakariko Shooting Gallery Adult', 'Kakariko Shooting Gallery Adult'),
#                      Child Kakariko Shooting Gallery?
                       ('Kakariko Shooting Gallery Exit Adult', 'Kakariko Village Adult'),
                       ('Kakariko Potion Shop Child', 'Kakariko Potion Shop Child'),
                       ('Kakariko Potion Shop Adult', 'Kakariko Potion Shop Adult'),
                       ('Kakariko Potion Shop Exit Child', 'Kakariko Village Child'),
                       ('Kakariko Potion Shop Exit Adult', 'Kakariko Village Adult'),
#                      Child Potion Shop Back?
                       ('Kakariko Potion Shop Back Adult', 'Kakariko Potion Shop Adult'),
#                      Child Potion Shop Back?
                       ('Kakariko Potion Shop Back Exit Adult', 'Kakariko Village Adult'),
#                      Child Grannys Potion Shop?
                       ('Grannys Potion Shop Adult', 'Grannys Potion Shop Adult'),
#                      Child Grannys Potion Shop?
                       ('Grannys Potion Shop Exit Adult', 'Kakariko Village Adult'),
                       ('Kakariko Bombable Grotto Child', 'Kakariko Bombable Grotto Child'),
                       ('Kakariko Bombable Grotto Adult', 'Kakariko Bombable Grotto Adult'),
                       ('Kakariko Bombable Grotto Exit Child', 'Kakariko Village Child'),
                       ('Kakariko Bombable Grotto Exit Adult', 'Kakariko Village Adult'),
                       ('Kakariko Back Grotto Child', 'Kakariko Back Grotto Child'),
                       ('Kakariko Back Grotto Adult', 'Kakariko Back Grotto Adult'),
                       ('Kakariko Back Grotto Exit Child', 'Kakariko Village Child'),
                       ('Kakariko Back Grotto Exit Adult', 'Kakariko Village Adult'),
                       ('Death Mountain Trail Child', 'Death Mountain Trail Child'),
                       ('Death Mountain Trail Adult', 'Death Mountain Trail Adult'),
                       ('Graveyard Child', 'Graveyard Child'),
                       ('Graveyard Adult', 'Graveyard Adult'),
                       ('Graveyard Exit Child', 'Kakariko Village Child'),
                       ('Graveyard Exit Adult', 'Kakariko Village Adult'),
                       ('Fairy Fountain Grave Child', 'Fairy Fountain Grave Child'),
                       ('Fairy Fountain Grave Adult', 'Fairy Fountain Grave Adult'),
                       ('Fairy Fountain Grave Exit Child', 'Graveyard Child'),
                       ('Fairy Fountain Grave Exit Adult', 'Graveyard Adult'),
                       ('Redead Grave Child', 'Redead Grave Child'),
                       ('Redead Grave Adult', 'Redead Grave Adult'),
                       ('Redead Grave Exit Child', 'Graveyard Child'),
                       ('Redead Grave Exit Adult', 'Graveyard Adult'),
                       ('Dampes House Child', 'Dampes House Child'),
                       ('Dampes House Adult', 'Dampes House Adult'),
                       ('Dampes House Exit Child', 'Graveyard Child'),
                       ('Dampes House Exit Adult', 'Graveyard Adult'),
                       ('Royal Family Tomb Child', 'Royal Family Tomb Child'),
                       ('Royal Family Tomb Adult', 'Royal Family Tomb Adult'),
                       ('Royal Family Tomb Exit Child', 'Graveyard Child'),
                       ('Royal Family Tomb Exit Adult', 'Graveyard Adult'),
                       ('Death Mountain Trail Exit Child', 'Kakariko Village Behind Gate Child'), # Child version of following entrance
                       ('Death Mountain Trail Exit Adult', 'Kakariko Village Adult'),
                       ('Dodongos Cavern Child', 'Dodongos Cavern Child'),
                       ('Dodongos Cavern Adult', 'Dodongos Cavern Adult'),
                       ('Mountain Storms Grotto Child', 'Mountain Storms Grotto Child'),
                       ('Mountain Storms Grotto Adult', 'Mountain Storms Grotto Adult'),
                       ('Mountain Storms Grotto Exit Child', 'Death Mountain Trail Child'),
                       ('Mountain Storms Grotto Exit Adult', 'Death Mountain Trail Adult'),
                       ('Mountain Fairy Child', 'Mountain Fairy Child'),
                       ('Mountain Fairy Adult', 'Mountain Fairy Adult'),
                       ('Mountain Fairy Exit Child', 'Death Mountain Trail Upper Child'),
                       ('Mountain Fairy Exit Adult', 'Death Mountain Trail Upper Adult'),
                       ('Mountain Bombable Grotto Child', 'Mountain Bombable Grotto Child'),
                       ('Mountain Bombable Grotto Adult', 'Mountain Bombable Grotto Adult'),
                       ('Mountain Bombable Grotto Exit Child', 'Death Mountain Trail Upper Child'),
                       ('Mountain Bombable Grotto Exit Adult', 'Death Mountain Trail Upper Adult'),
                       ('Mountain Owl Child', 'Kakariko Village Child'),
#                      Adult Owl?
                       ('Death Mountain Crater Child', 'Death Mountain Crater Upper Child'),
                       ('Death Mountain Crater Adult', 'Death Mountain Crater Upper Adult'),
                       ('Death Mountain Crater Exit Child', 'Death Mountain Trail Upper Child'),
                       ('Death Mountain Crater Exit Adult', 'Death Mountain Trail Upper Adult'),
                       ('Goron City Child', 'Goron City Child'),
                       ('Goron City Adult', 'Goron City Adult'),
                       ('Goron City Exit Child', 'Death Mountain Trail Child'),
                       ('Goron City Exit Adult', 'Death Mountain Trail Adult'),
                       ('Goron City to Lost Woods Child', 'Lost Woods Child'),
                       ('Goron City to Lost Woods Adult', 'Lost Woods Adult'),
                       ('Goron Shop Child', 'Goron Shop Child'),
                       ('Goron Shop Adult', 'Goron Shop Adult'),
                       ('Goron Shop Exit Child', 'Goron City Child'),
                       ('Goron Shop Exit Adult', 'Goron City Adult'),
#                      ('Goron City Grotto Child', 'Goron City Grotto Child'),
                       ('Goron City Grotto Adult', 'Goron City Grotto Adult'),
#                      ('Goron City Grotto Exit Child', 'Goron City Lava Child'),
                       ('Goron City Grotto Exit Adult', 'Goron City Lava Adult'),
#                      ('Goron City to Crater Child', 'Death Mountain Crater Lower Child'),
                       ('Goron City to Crater Adult', 'Death Mountain Crater Lower Adult'),
#                      ('Crater to Goron City Child', 'Goron City Darunia Child'),
                       ('Crater to Goron City Adult', 'Goron City Darunia Adult'),
#                      Child Crater Fairy?
                       ('Crater Fairy Adult', 'Crater Fairy Adult'),
#                      Child Crater Fairy?
                       ('Crater Fairy Exit Adult', 'Death Mountain Crater Lower Adult'),
                       ('Top of Crater Grotto Child', 'Top of Crater Grotto Child'),
                       ('Top of Crater Grotto Adult', 'Top of Crater Grotto Adult'),
                       ('Top of Crater Grotto Exit Child', 'Death Mountain Crater Upper Child'),
                       ('Top of Crater Grotto Exit Adult', 'Death Mountain Crater Upper Adult'),
#                      Child Hammer Grotto?
                       ('Crater Hammer Grotto Adult', 'Crater Hammer Grotto Adult'),
#                      Child Hammer Grotto?
                       ('Crater Hammer Grotto Exit Adult', 'Death Mountain Crater Lower Adult'),
                       ('Market Exit Child', 'Hyrule Field Child'),
                       ('Market Exit Adult', 'Hyrule Field Adult'),
                       ('Guard House Child', 'Guard House Child'),
                       ('Guard House Adult', 'Guard House Adult'),
                       ('Guard House Exit Child', 'Market Entrance Child'),
                       ('Guard House Exit Adult', 'Market Entrance Adult'),
                       ('Market Child', 'Market Child'),
                       ('Market Adult', 'Market Adult'),
                       ('Market to Market Entrance Child', 'Market Entrance Child'),
                       ('Market to Market Entrance Adult', 'Market Entrance Adult'),
                       ('Back Alley South Child', 'Back Alley Child'),
#                      Adult Back Alley?
                       ('Back Alley South Exit Child', 'Market Child'),
#                      Adult Back Alley?
                       ('Back Alley North Child', 'Back Alley Child'),
#                      Adult Back Alley?
                       ('Back Alley North Exit Child', 'Market Child'),
#                      Adult Back Alley?
                       ('Bombchu Shop Child', 'Bombchu Shop Child'),
#                      Adult Bombchu Shop?
                       ('Bombchu Shop Exit Child', 'Back Alley Child'),
#                      Adult Bombchu Shop?
                       ('Dog Lady House Child', 'Dog Lady House Child'),
#                      Adult Dog Lady House?
                       ('Dog Lady House Exit Child', 'Back Alley Child'),
#                      Adult Dog Lady House?
                       ('Back Alley House Child', 'Back Alley House Child'),
#                      Adult Back Alley House?
                       ('Back Alley House Exit Child', 'Back Alley Child'),
#                      Adult Back Alley House?
                       ('Market Bazaar Child', 'Market Bazaar Child'),
#                      Adult Market Bazaar?
                       ('Market Bazaar Exit Child', 'Market Child'),
#                      Adult Market Bazaar?
                       ('Market Potion Shop Child', 'Market Potion Shop Child'),
#                      Adult Market Potion Shop?
                       ('Market Potion Shop Exit Child', 'Market Child'),
#                      Adult Market Potion Shop?
                       ('Happy Mask Shop Child', 'Happy Mask Shop Child'),
#                      Adult Happy Mask Shop?
                       ('Happy Mask Shop Exit Child', 'Market Child'),
#                      Adult Happy Mask Shop?
                       ('Market Shooting Gallery Child', 'Market Shooting Gallery Child'),
#                      Adult Market Shooting Gallery?
                       ('Market Shooting Gallery Exit Child', 'Market Child'),
#                      Adult Market Shooting Gallery?
                       ('Bombchu Bowling Child', 'Bombchu Bowling Child'),
#                      Adult Bombchu Bowling?
                       ('Bombchu Bowling Exit Child', 'Market Child'),
#                      Adult Bombchu Bowling?
                       ('Treasure Chest Game Child', 'Treasure Chest Game Child'),
#                      Adult Treasure Chest Game?
                       ('Treasure Chest Game Exit Child', 'Market Child'),
#                      Adult Treasure Chest Game?
                       ('Hyrule Castle Child', 'Hyrule Castle Child'),
                       ('Ganons Castle Adult', 'Ganons Castle Adult'),
                       ('Hyrule Castle Exit Child', 'Market Child'),
                       ('Ganons Castle Exit Adult', 'Market Adult'),
                       ('Hyrule Castle Fairy Child', 'Hyrule Castle Fairy Child'),
#                      Adult Fairy?
#                      Child Fairy?
                       ('Ganons Castle Fairy Adult', 'Ganons Castle Fairy Adult'),
                       ('Hyrule Castle Fairy Exit Child', 'Hyrule Castle Child'),
                       ('Ganons Castle Fairy Exit Adult', 'Ganons Castle Adult'),
                       ('Hyrule Castle Storms Grotto Child', 'Hyrule Castle Storms Grotto Child'),
#                      Adult Hyrule Castle Storms Grotto?
                       ('Hyrule Castle Storms Grotto Exit Child', 'Hyrule Castle Upper Child'),
#                      Adult Hyrule Castle Storms Grotto?
                       ('Castle Caught by Guards Child', 'Hyrule Castle Child'),
#                      Adult Castle Caught by Guards? I think this crashes currently?
                       ('Hyrule Castle Courtyard Child', 'Hyrule Castle Courtyard Child'),
#                      Adult Hyrule Castle Courtyard Child?    # See Inside Ganons Castle Exit for this return entrance.
                       ('Courtyard Caught by Guards Child', 'Hyrule Castle Upper Child'),
#                      Adult Courtyard Caught by Guards?
                       ('Zeldas Courtyard Child', 'Zeldas Courtyard Child'),
#                      Adult Zeldas Courtyard?
                       ('Zeldas Courtyard Exit Child', 'Hyrule Castle Courtyard Child'),
#                      Adult Zeldas Courtyard?
                       ('Impa Exit Child', 'Hyrule Field Child'),
#                      Adult Zeldas Courtyard?
                       ('Outside Temple of Time Child', 'Outside Temple of Time Child'),
                       ('Outside Temple of Time Adult', 'Outside Temple of Time Adult'),
                       ('Outside Temple to Market Child', 'Market Child'),
                       ('Outside Temple to Market Adult', 'Market Adult'),
                       ('Temple of Time Child', 'Temple of Time Child'),
                       ('Temple of Time Adult', 'Temple of Time Adult'),
                       ('Temple of Time Exit Child', 'Outside Temple of Time Child'),
                       ('Temple of Time Exit Adult', 'Outside Temple of Time Adult')
                      ]

# non shuffled dungeons
# no attempt was made to handle coming and going from potentially shuffled boss loading zones
# and no attempt was made to muck with the logic for potentially randomized spirit temple hand loading zones
default_dungeon_connections = [('Deku Tree Child', 'Deku Tree Child'),
#                              Deku Tree Adult?
                               ('Deku Tree Exit Child', 'Kokiri Forest Child'),
#                              Deku Tree Adult?
                               ('Dodongos Cavern Child', 'Dodongos Cavern Child'),
                               ('Dodongos Cavern Adult', 'Dodongos Cavern Adult'),
                               ('Dodongos Cavern Exit Child', 'Death Mountain Trail Child'),
                               ('Dodongos Cavern Exit Adult', 'Death Mountain Trail Adult'),
                               ('Jabu Jabus Belly Child', 'Jabu Jabus Belly Child'),
#                              Jabu Jabu Adult?
                               ('Jabu Jabus Belly Exit Child', 'Zoras Fountain Child'),
#                              Jabu Jabu Adult?
                               ('Bottom of the Well Child', 'Bottom of the Well Child'),
#                              Bottom of the Well Adult?
                               ('Bottom of the Well Exit Child', 'Kakariko Village Child'),
#                              Bottom of the Well Adult?
#                              Forest Temple Child?
                               ('Forest Temple Adult', 'Forest Temple Adult'),
#                              Forest Temple Child?
                               ('Forest Temple Exit Adult', 'Sacred Forest Meadow Adult'),
#                              ('Fire Temple Child', 'Fire Temple Child'),
                               ('Fire Temple Adult', 'Fire Temple Adult'),
#                              ('Fire Temple Exit Child', 'Death Mountain Crater Near Temple Child'),
                               ('Fire Temple Exit Adult', 'Death Mountain Crater Central Adult'),
#                              Water Temple Child?
                               ('Water Temple Adult', 'Water Temple Adult'),
#                              Water Temple Child?
                               ('Water Temple Exit Adult', 'Lake Hylia Child'),
                               ('Shadow Temple Child', 'Shadow Temple Child'),
                               ('Shadow Temple Adult', 'Shadow Temple Adult'),
                               ('Shadow Temple Exit Child', 'Shadow Temple Warp Child'),
                               ('Shadow Temple Exit Adult', 'Shadow Temple Warp Adult'),
                               ('Spirit Temple Child', 'Spirit Temple Child'),
                               ('Spirit Temple Adult', 'Spirit Temple Adult'),
                               ('Spirit Temple Exit Child', 'Desert Colossus Song Child'),
                               ('Spirit Temple Exit Adult', 'Desert Colossus Song Adult'),
                               ('Spirit Temple Right Hand Child', 'Spirit Child Upper Child'), # Silver Gauntlets Side
                               ('Spirit Temple Right Hand Adult', 'Spirit Child Upper Adult'),
                               ('Spirit Right Hand Exit Child', 'Desert Colossus Right Hand Child'),
                               ('Spirit Right Hand Exit Adult', 'Desert Colossus Right Hand Adult'),
#                              Child Left Hand? # Mirror Shield Side
                               ('Spirit Temple Left Hand Adult', 'Spirit Adult Upper Adult'),
#                              Child Left Hand?
                               ('Spirit Left Hand Exit Adult', 'Desert Colossus Left Hand Adult'),
#                              Ice Cavern Child?
                               ('Ice Cavern Adult', 'Ice Cavern Adult'),
#                              Ice Cavern Child?
                               ('Ice Cavern Exit Adult', 'Zoras Fountain Adult'),
#                              GTG Child?
                               ('Gerudo Training Grounds Adult', 'Gerudo Training Grounds Adult'),
#                              GTG Child?
                               ('Gerudo Training Grounds Exit Adult', 'Fortress Entry from GTG Adult'),
#                              Child Inside Ganons Castle?
                               ('Rainbow Bridge', 'Inside Ganons Castle Adult'),
                               ('Hyrule Castle Courtyard Exit Child', 'Hyrule Castle Upper Child'),
                               ('Inside Ganons Castle Exit Adult', 'Ganons Castle Adult')    # Normally this spawns over lava (not a softlock because you can save warp, but still). BQ moved this entrance to the other side of the bridge, so I've decided to just pretend that's happening.
                              ]
