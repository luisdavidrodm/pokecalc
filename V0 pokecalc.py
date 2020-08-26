
import math, time, sys, random

############### menus ###############
def start():
    '''Excutes the main menu.'''
    print('''\n    [MAIN MENU]
    1: STAT (Start STATS Calculation)
    2: IV   (Start IVS Calculation)
    3: EV   (Start EVS Calculation)
    4: HELP (Find more options)
    5: EXIT (Finish the program)\n''')
    while True:
        startvar = input('''What do you want to do?:''').upper()
        if startvar == 'STAT' or startvar == '1':
            print('\n» [STATS CALCULATOR]')
            startvar = 'STAT'
            break
        elif startvar == 'IV' or startvar == '2':
            print('\n» [IVS CALCULATOR]')
            startvar = 'IV'
            break
        elif startvar == 'EV' or startvar == '3':
            print('\n» [EVS CALCULATOR]')
            startvar = 'EV'
            break
        elif startvar == 'HELP' or startvar == '4':
            help()
        elif startvar == 'EXIT' or startvar == '5':
            sys.stdout.write("»[GOODBYE!].")
            time.sleep(0.1)
            sys.stdout.write(".")
            time.sleep(0.1)
            sys.stdout.write(".")
            time.sleep(0.1)
            sys.exit()
        else:
            print('{} Enter a valid option.'.format(wronginput))
    print('''  [Please enter the information requested below]
  [Write EXIT to go back to main menu]\n''')
    inputgather(startvar)

def help():
    '''Excutes the help menu.'''
    helpvar = input('''\n    [HELP MENU]
    1: ABOUT (About this app)
    2: BACK  (Go back)

What do you want to do?: ''').upper()
    if helpvar == 'ABOUT' or helpvar == '1':
        print('\n» [VERSION] Alpha v1.0\n  Developed by SpaceRM.')
        help()
    elif helpvar == 'BACK' or helpvar == '2':
        start()
    else:
        print('» [WRONG INPUT] Enter a valid option.')
        help()

def exitprint():
    '''Returns to main menu.'''
    sys.stdout.write("» [RETURNING TO MAIN MENU].")
    time.sleep(0.1)
    sys.stdout.write(".")
    time.sleep(0.1)
    sys.stdout.write(".\n")
    time.sleep(0.1)
    start()

############### input ###############
def inputgather(startvar):
    '''Routine that gathers and checks the information needed and then run main routines to finally print the results.'''
    while True:
       specie = input('POKEMON SPECIE: ').upper()
       if specie == 'EXIT':
           exitprint()
       elif basestatsdic.get(specie) == None:
           print('{}No match found.'.format(wronginput))
       else:
           break
    while True:
       level = (input('LEVEL: '))
       if level.upper() == 'EXIT':
           exitprint()
       else:
           try:
               level = int(level)
               if not 1 <= level <= 100:
                   raise Exception('Level must be between 1 and 100')
           except ValueError:
               print('{}Only integers are allowed.'.format(wronginput))
           except Exception:
               print('{}Level must be between 1 and 100.'.format(wronginput))
           else:
               break
    while True:
        nature = input('NATURE: ').upper()
        if nature == 'EXIT':
            exitprint()
        elif naturedic.get(nature) == None:
            print('{}No match found.'.format(wronginput))
        else:
            break
    if startvar == 'STAT':
        ivs = gather35('IV', 31)
        evs = gather35('EV', 255)
        results = statscalc35(specie, level, nature, ivs, evs)
    elif startvar == 'IV':
        evs = gather35('EV', 255)
        maxval = ' '.join(list(map(str,statscalc35(specie, level, nature, list(map(lambda y: 31, range(6))), evs))))
        minval = ' '.join(list(map(str,statscalc35(specie, level, nature, list(map(lambda y: 0, range(6))), evs))))
        stats = gather35('STAT',maxval,minval)
        results = xvscalc35(specie, level, nature, stats, evs, 'EV')
    elif startvar == 'EV':
        ivs = gather35('IV', 31)
        maxval = ' '.join(list(map(str,statscalc35(specie, level, nature, ivs, list(map(lambda y: 255, range(6)))))))
        minval = ' '.join(list(map(str,statscalc35(specie, level, nature, ivs, list(map(lambda y: 0, range(6)))))))
        stats = gather35('STAT',maxval,minval)
        results = xvscalc35(specie, level, nature, stats, ivs, 'IV')
    statslist = ['HP', 'ATK', 'DEF', 'SPA', 'SPD', 'SPE']
    if naturedic.get(nature) != (0, 0):
        statchanges = ' ({}x1.1 & {}x0.9)'.format(statslist[naturedic.get(nature)[0]],statslist[naturedic.get(nature)[1]])
    else:
        statchanges = ' (No modifiers)'
    print('''\n{}NAME: {}
            LEVEL: {}
            NATURE: {}'''.format(resultsestr,specie,level,nature)+statchanges)
    if startvar == 'STAT' or results['MAX'] == results['MIN']:
        print('  [{}S] HP ATK DEF SPA SPD SPE\n  [{}S] '.format(startvar,startvar)+' '.join(list(map(str,results))))
    else:
        print('  [{}S] HP ATK DEF SPA SPD SPE\n  [MAX] {}\n  [MIN] {}'.format(startvar,' '.join(list(map(str,results['MAX']))),' '.join(list(map(str,results['MIN'])))))
        print('\n  [STATS] HP ATK DEF SPA SPD SPE\n  [MAX]   {}\n  [MIN]   {}'.format(maxval,minval))
    input('\n» [Press ENTER to go back to main menu]')
    exitprint()

def gather35(name, maxval, minval=0):
    '''Routine used by inputgather() for gathering and checking the STATS, EVS or IVS needed to run main routines.'''
    while True:
        x = input('{}S: HP ATK DEF SPA SPD SPE\n{}S: '.format(name, name)).split()
        if ''.join(x).upper() == 'EXIT':
            exitprint()
        elif len(x) == 0:
            print('''{}You entered nothing.
  But you must enter six values.'''.format(wronginput))
            print(example35(name, maxval, minval))
        elif len(x) != 6:
            print('''{}You entered: {}
  That is {} values, but there must be only six values.'''.format(wronginput, x, len(x)))
            print(example35(name, maxval, minval))
        else:
            try:
                x = list(map(int, x))
                if name == 'STAT':
                    list(map(rangecheck, x, list(map(int,minval.split())), list(map(int,maxval.split()))))
                else:
                    list(map(rangecheck, x, list(map(lambda y: 0, range(6))), list(map(lambda y: maxval, range(6)))))
                if name == 'EV' and sum(x) > 510:
                    raise Exception('Values sum is greater than 510')
            except ValueError:
                print('''{}You entered: {}
  But only just integers are allowed.'''.format(wronginput, x))
                print(example35(name, maxval, minval))
            except SyntaxError:
                print('''{}You entered: {}
  But values are out of the range.'''.format(wronginput, x))
                print(example35(name, maxval, minval))
            except Exception:
                print('''{}You entered: {}
  But the sum of the values ({}) is greater than 510 in total.'''.format(wronginput, x, sum(x)))
                print(example35(name, maxval, minval))
            else:
                return x

def example35(name, maxval, minval=0):
    '''Returns a string with an example of a correct input for any case.'''
    if name == 'STAT':
        return '''  With maxium and minimun values allowed being:
  [MAX] {}
  [MIN] {}'''.format(maxval, minval)
    else:
        if name == 'EV':
            s = 0
            gen = (random.randint(0,min(510-s,255)) for i in range(6))
            res = []
            for el in gen:
                res.append(el)
                s+=el
            example = res
            ifev = '\n  And the sum of the values must not exceed 510 in total.'
        else:
            example = random.sample(range(maxval), 6)
            ifev = ''
        return '''  The values must be between {} and {}.{}
 {}'''.format(minval, maxval, ifev, examplestr)+' '.join(list(map(str, example)))

def rangecheck(var, minval, maxval):
    '''Checks is a variable is between two values.'''
    if not minval <= var <= maxval:
        raise SyntaxError('Value not in range')

############### main routines ###############
def statscalc35(specie, level, nature, ivs, evs):
    '''Return the STATS of a Pokemon from Generation III onwards in a list.'''
    stats=[]
    for i in range(6):
        stat = ((2*basestatsdic.get(specie)[i])+ivs[i]+math.floor(evs[i]/4.0))*level/100.0
        if i == 0:
            if specie == "SHEDINJA":
                stats.append(1)
                continue
            else:
                stat = math.floor(stat+level+10)
        else:
            stat = math.floor(stat+5)
        stats.append(stat)
    if naturedic.get(nature) != (0, 0):
        stats[naturedic.get(nature)[0]] = math.floor(stats[naturedic.get(nature)[0]]*(1.1))
        stats[naturedic.get(nature)[1]] = math.floor(stats[naturedic.get(nature)[1]]*(0.9))
    return list(map(int, stats))

def xvscalc35(specie, level, nature, stats, zvs, name):
    '''Return the MAX and MIN; IVS or EVS of a Pokemon from Generation III onwards in a dict.
       Depending wheter you gave IVS or EVS in zvs & name.'''
    xvs = {'MIN':[], 'MAX':[]}
    xvsiter = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[]}
    if name == 'IV':
        for i in range(256):
            statsiter = statscalc35(specie, level, nature, zvs, list(map(lambda y: i, range(6))))
            for j in range(6):
                if stats[j] == statsiter[j]:
                    xvsiter[j].append(i)
    else:
        for i in range(32):
            statsiter = statscalc35(specie, level, nature, list(map(lambda y: i, range(6))), zvs)
            for j in range(6):
                if stats[j] == statsiter[j]:
                    xvsiter[j].append(i)
    for j in range(6):
        xvs['MIN'].append(min(list(xvsiter.values())[j]))
        xvs['MAX'].append(max(list(xvsiter.values())[j]))
    return xvs

############### database ###############
if True:

    naturedic = {'FUERTE': (0, 0), 'HARDY': (0, 0), 'OSADA': (2, 1), 'BOLD': (2, 1),
    'MODESTA': (3, 1), 'MODEST': (3, 1), 'SERENA': (4, 1), 'CALM': (4, 1), 'MIEDOSA': (5, 1), 'TIMID': (5, 1),
    'HURANA': (1, 2), 'LONELY': (1, 2), 'DOCIL': (0, 0), 'DOCILE': (0, 0), 'AFABLE': (3, 2), 'MILD': (3, 2),
    'AMABLE': (4, 2), 'GENTLE': (4, 2), 'ACTIVA': (5, 2), 'HASTY': (5, 2), 'FIRME': (1, 3), 'ADAMANT': (1, 3),
    'AGITADA': (2, 3), 'IMPISH': (2, 3), 'TIMIDA': (0, 0), 'BASHFUL': (0, 0), 'CAUTA': (4, 3), 'CAREFUL': (4, 3),
    'ALEGRE': (5, 3), 'JOLLY': (5, 3), 'PICARA': (1, 4), 'NAUGHTY': (1, 4), 'FLOJA': (2, 4), 'LAX': (2, 4),
    'ALOCADA': (3, 4), 'RASH': (3, 4), 'RARA': (0, 0), 'QUIRKY': (0, 0), 'INGENUA': (5, 4), 'NAIVE': (5, 4),
    'AUDAZ': (1, 5), 'BRAVE': (1, 5), 'PLACIDA': (2, 5), 'RELAXED': (2, 5), 'MANSA': (3, 5), 'QUIET': (3, 5),
    'GROSERA': (4, 5), 'SASSY': (4, 5), 'SERIA': (0, 0), 'SERIOUS': (0, 0)}

    basestatsdic = {"BULBASAUR":(45,49,49,65,65,45), "IVYSAUR":(60,62,63,80,80,60),
    "VENASAUR":(80,82,83,100,100,80), "CHARMANDER":(39,52,43,60,50,65),
    "CHARMELEON":(58,64,58,80,65,80), "CHARIZARD":(78,84,78,109,85,100),
    "SQUIRTLE":(44,48,65,50,64,43), "WARTORTLE":(59,63,80,65,80,58),
    "BLASTOISE":(79,83,100,85,105,78), "CATERPIE":(45,30,35,20,20,45),
    "METAPOD":(50,20,55,25,25,30), "BUTTERFREE":(60,45,50,80,80,70),
    "WEEDLE":(40,35,30,20,20,50), "KAKUNA":(45,25,50,25,25,35),
    "BEEDRILL":(65,80,40,45,80,75), "PIDGEY":(40,45,40,35,35,56),
    "PIDGEOTTO":(63,60,55,50,50,71), "PIDGEOT":(83,80,75,70,70,91),
    "RATTATA":(30,56,35,25,35,72), "RATICATE":(55,81,60,50,70,97),
    "SPEAROW":(40,60,30,31,31,70), "FEAROW":(65,90,65,61,61,100),
    "EKANS":(35,60,44,40,54,55), "ARBOK":(60,85,69,65,79,80),
    "PIKACHU":(35,55,30,50,40,90), "RAICHU":(60,90,55,90,80,100),
    "SANDSHREW":(50,75,85,20,30,40), "SANDSLASH":(75,100,110,45,55,65),
    "NIDORANH":(55,47,52,40,40,41), "NIDORINA":(70,62,67,55,55,56),
    "NIDOQUEEN":(90,82,87,75,85,76), "NIDORANM":(46,57,40,40,40,50),
    "NIDORINO":(61,72,57,55,55,65), "NIDOKING":(81,92,77,85,75,85),
    "CLEFAIRY":(70,45,48,60,65,35), "CLEFABLE":(95,70,73,85,90,60),
    "VULPIX":(38,41,40,50,65,65), "NINETALES":(73,76,75,81,100,100),
    "JIGGLYPUFF":(115,45,20,45,25,20), "WIGGLYTUFF":(140,70,45,75,50,45),
    "ZUBAT":(40,45,35,30,40,55), "GOLBAT":(75,80,70,65,75,90),
    "ODDISH":(45,50,55,75,65,30), "GLOOM":(60,65,70,85,75,40),
    "VILEPLUME":(75,80,85,100,90,50), "PARAS":(35,70,55,45,55,25),
    "PARASECT":(60,95,80,60,80,30), "VENONAT":(60,55,50,40,55,45),
    "VENOMOTH":(70,65,60,90,75,90), "DIGLETT":(10,55,25,35,45,95),
    "DUGTRIO":(35,80,50,50,70,120), "MEOWTH":(40,45,35,40,40,90),
    "PERSIAN":(65,70,60,65,65,115), "PSYDUCK":(50,52,48,65,50,55),
    "GOLDUCK":(80,82,78,95,80,85), "MANKEY":(40,80,35,35,45,70),
    "PRIMEAPE":(65,105,60,60,70,95), "GROWLITHE":(55,70,45,70,50,60),
    "ARCANINE":(90,110,80,100,80,95), "POLIWAG":(40,50,40,40,40,90),
    "POLIWHIRL":(65,65,65,50,50,90), "POLIWRATH":(90,85,95,70,90,70),
    "ABRA":(25,20,15,105,55,95), "KADABRA":(40,35,30,120,70,105),
    "ALAKAZAM":(55,50,45,135,85,120), "MACHOP":(70,80,50,35,35,35),
    "MACHOKE":(80,100,70,50,60,45), "MACHAMP":(90,130,80,65,85,55),
    "BELLSPROUT":(50,75,35,70,30,40), "WEEPINBELL":(65,90,50,85,45,55),
    "VICTREEBEL":(80,105,65,100,60,70), "TENTACOOL":(40,40,35,50,100,70),
    "TENTACRUEL":(80,70,65,80,120,100), "GEODUDE":(40,80,100,30,30,20),
    "GRAVELER":(65,95,115,45,45,35), "GOLEM":(80,110,130,55,65,45),
    "PONYTA":(50,85,55,65,65,90), "RAPIDASH":(65,100,70,80,80,105),
    "SLOWPOKE":(90,65,65,40,40,15), "SLOWBRO":(95,75,110,100,80,30),
    "MAGNEMITE":(25,35,70,95,55,45), "MAGNETON":(50,60,95,120,70,70),
    "FARFETCH'D":(52,65,55,58,62,60), "DODUO":(35,85,45,35,35,75),
    "DODRIO":(60,110,70,60,60,100), "SEEL":(65,45,55,45,70,45),
    "DEWGONG":(90,70,80,70,95,70), "GRIMER":(80,80,50,40,50,25),
    "MUK":(105,105,75,65,100,50), "SHELLDER":(30,65,100,45,25,40),
    "CLOYSTER":(50,95,180,85,45,70), "GASTLY":(30,35,30,100,35,80),
    "HAUNTER":(45,50,45,115,55,95), "GENGAR":(60,65,60,130,75,110),
    "ONIX":(35,45,160,30,45,70), "DROWZEE":(60,48,45,43,90,42),
    "HYPNO":(85,73,70,73,115,67), "KRABBY":(30,105,90,25,25,50),
    "KINGLER":(55,130,115,50,50,75), "VOLTORB":(40,30,50,55,55,100),
    "ELECTRODE":(60,50,70,80,80,140), "EXEGGCUTE":(60,40,80,60,45,40),
    "EXEGGUTOR":(95,95,85,125,65,55), "CUBONE":(50,50,95,40,50,35),
    "MAROWAK":(60,80,110,50,80,45), "HITMONLEE":(50,120,53,35,110,87),
    "HITMONCHAN":(50,105,79,35,110,76), "LICKITUNG":(90,55,75,60,75,30),
    "KOFFING":(40,65,95,60,45,35), "WEEZING":(65,90,120,85,70,60),
    "RHYHORN":(80,85,95,30,30,25), "RHYDON":(105,130,120,45,45,40),
    "CHANSEY":(250,5,5,35,105,50), "TANGELA":(65,55,115,100,40,60),
    "KANGASKHAN":(105,95,80,40,80,90), "HORSEA":(30,40,70,70,25,60),
    "SEADRA":(55,65,95,95,45,85), "GOLDEEN":(45,67,60,35,50,63),
    "SEAKING":(80,92,65,65,80,68), "STARYU":(30,45,55,70,55,85),
    "STARMIE":(60,75,85,100,85,115), "MR.,MIME":(40,45,65,100,120,90),
    "SCYTHER":(70,110,80,55,80,105), "JYNX":(65,50,35,115,95,95),
    "ELECTABUZZ":(65,83,57,95,85,105), "MAGMAR":(65,95,57,100,85,93),
    "PINSIR":(65,125,100,55,70,85), "TAUROS":(75,100,95,40,70,110),
    "MAGIKARP":(20,10,55,15,20,80), "GYARADOS":(95,125,79,60,100,81),
    "LAPRAS":(130,85,80,85,95,60), "DITTO":(48,48,48,48,48,48),
    "EEVEE":(55,55,50,45,65,55), "VAPOREON":(130,65,60,110,95,65),
    "JOLTEON":(65,65,60,110,95,130), "FLAREON":(65,130,60,95,110,65),
    "PORYGON":(65,60,70,85,75,40), "OMANYTE":(35,40,100,90,55,35),
    "OMASTAR":(70,60,125,115,70,55), "KABUTO":(30,80,90,55,45,55),
    "KABUTOPS":(60,115,105,65,70,80), "AERODACTYL":(80,105,65,60,75,130),
    "SNORLAX":(160,110,65,65,110,30), "ARTICUNO":(90,85,100,95,125,85),
    "ZAPDOS":(90,90,85,125,90,100), "MOLTRES":(90,100,90,125,85,90),
    "DRATINI":(41,64,45,50,50,50), "DRAGONAIR":(61,84,65,70,70,70),
    "DRAGONITE":(91,134,95,100,100,80), "MEWTWO":(106,110,90,154,90,130),
    "MEW":(100,100,100,100,100,100), "CHIKORITA":(45,49,65,49,65,45),
    "BAYLEEF":(60,62,80,63,80,60), "MEGANIUM":(80,82,100,83,100,80),
    "CYNDAQUIL":(39,52,43,60,50,65), "QUILAVA":(58,64,58,80,65,80),
    "TYPHLOSION":(78,84,78,109,85,100), "TOTODILE":(50,65,64,44,48,43),
    "CROCONAW":(65,80,80,59,63,58), "FERALIGATR":(85,105,100,79,83,78),
    "SENTRET":(35,46,34,35,45,20), "FURRET":(85,76,64,45,55,90),
    "HOOTHOOT":(60,30,30,36,56,50), "NOCTOWL":(100,50,50,76,96,70),
    "LEDYBA":(40,20,30,40,80,55), "LEDIAN":(55,35,50,55,110,85),
    "SPINARAK":(40,60,40,40,40,30), "ARIADOS":(70,90,70,60,60,40),
    "CROBAT":(85,90,80,70,80,130), "CHINCHOU":(75,38,38,56,56,67),
    "LANTURN":(125,58,58,76,76,67), "PICHU":(20,40,15,35,35,60),
    "CLEFFA":(50,25,28,45,55,15), "IGGLYBUFF":(90,30,15,40,20,15),
    "TOGEPI":(35,20,65,40,65,20), "TOGETIC":(55,40,85,80,105,40),
    "NATU":(40,50,45,70,45,70), "XATU":(65,75,70,95,70,95),
    "MAREEP":(55,40,40,65,45,35), "FLAAFFY":(70,55,55,80,60,45),
    "AMPHAROS":(90,75,75,115,90,55), "BELLOSSOM":(75,80,85,90,100,50),
    "MARILL":(70,20,50,20,50,40), "AZUMARILL":(100,50,80,50,80,50),
    "SUDOWOODO":(70,100,115,30,65,30), "POLITOED":(90,75,75,90,100,70),
    "HOPPIP":(35,35,40,35,55,50), "SKIPLOOM":(55,45,50,45,65,80),
    "JUMPLUFF":(75,55,70,55,85,110), "AIPOM":(55,70,55,40,55,85),
    "SUNKERN":(30,30,30,30,30,30), "SUNFLORA":(75,75,55,105,85,30),
    "YANMA":(65,65,45,75,45,95), "WOOPER":(55,45,45,25,25,15),
    "QUAGSIRE":(95,85,85,65,65,35), "ESPEON":(65,65,60,130,95,110),
    "UMBREON":(95,65,110,60,130,65), "MURKROW":(60,85,42,85,42,91),
    "SLOWKING":(95,75,80,100,110,30), "MISDREAVUS":(60,60,60,85,85,85),
    "UNOWN":(48,72,48,72,48,48), "WOBBUFFET":(190,33,58,33,58,33),
    "GIRAFARIG":(70,80,65,90,65,85), "PINECO":(50,65,90,35,35,15),
    "FORRESTRESS":(75,90,140,60,60,40), "DUNSPARCE":(100,70,70,65,65,45),
    "GLIGAR":(65,75,105,35,65,85), "STEELIX":(75,85,200,55,65,30),
    "SNUBBULL":(60,80,50,40,40,30), "GRANBULL":(90,120,75,60,60,45),
    "QWILFISH":(65,95,75,55,55,85), "SCIZOR":(70,130,100,55,80,65),
    "SHUCKLE":(20,10,230,10,230,5), "HERACROSS":(80,125,75,40,95,85),
    "SNEASEL":(55,95,55,35,75,115), "TEDDIURSA":(60,80,50,50,50,40),
    "URSARING":(90,130,75,75,75,55), "SLUGMA":(40,40,40,70,40,20),
    "MAGCARGO":(50,50,120,80,80,30), "SWINUB":(50,50,40,30,30,50),
    "PILOSWINE":(100,100,80,60,60,50), "CORSOLA":(55,55,85,65,85,35),
    "REMORAID":(35,65,35,65,35,65), "OCTILLERY":(75,105,75,105,75,45),
    "DELIBIRD":(45,55,45,65,45,75), "MANTINE":(65,40,70,80,140,70),
    "SKARMORY":(65,80,140,40,70,70), "HOUNDOUR":(45,60,30,80,50,65),
    "HOUNDOOM":(75,90,50,110,80,95), "KINGDRA":(75,95,95,95,95,85),
    "PHANPY":(90,60,60,40,40,40), "DONPHAN":(90,120,120,60,60,50),
    "PORYGON2":(85,80,90,105,95,60), "STANTLER":(73,95,62,85,65,85),
    "SMEARGLE":(55,20,35,20,45,75), "TYROGUE":(35,35,35,35,35,35),
    "HITMONTOP":(50,95,95,35,110,70), "SMOOCHUM":(45,30,15,85,65,65),
    "ELEKID":(45,63,37,65,55,95), "MAGBY":(45,75,37,70,55,83),
    "MILTANK":(95,80,105,40,70,100), "BLISSEY":(255,10,10,75,135,55),
    "RAIKOU":(90,85,75,115,100,115), "ENTEI":(115,115,85,90,75,100),
    "SUICUNE":(100,75,115,90,115,85), "LARVITAR":(50,64,50,45,50,41),
    "PUPITAR":(70,84,70,65,70,51), "TYRANITAR":(100,134,110,95,100,61),
    "LUGIA":(106,90,130,90,154,110), "HO-OH":(106,130,90,110,154,90),
    "CELEBI":(100,100,100,100,100,100), "TREECKO":(40,45,35,65,55,70),
    "GROVYLE":(50,65,45,85,65,95), "SCEPTILE":(70,85,65,105,85,120),
    "TORCHIC":(45,60,40,70,50,45), "COMBUSKEN":(60,85,60,85,60,55),
    "BLAZIKEN":(80,120,70,110,70,80), "MUDKIP":(50,70,50,50,50,40),
    "MARSHTOMP":(70,85,70,60,70,50), "SWAMPERT":(100,110,90,85,90,60),
    "POOCHYENA":(35,55,35,30,30,35), "MIGHTYENA":(70,90,70,60,60,70),
    "ZIGZAGOON":(38,30,41,30,41,60), "LINOONE":(78,70,61,50,61,100),
    "WURMPLE":(45,45,35,20,30,20), "SILCOON":(50,35,55,25,25,15),
    "BEAUTIFLY":(60,70,50,90,50,65), "CASCOON":(50,35,55,25,25,15),
    "DUSTOX":(60,50,70,50,90,65), "LOTAD":(40,30,30,40,50,30),
    "LOMBRE":(60,50,50,60,70,50), "LUDICOLO":(80,70,70,90,100,70),
    "SEEDOT":(40,40,50,30,30,30), "NUZLEAF":(70,70,40,60,40,60),
    "SHIFTRY":(90,100,60,90,60,80), "TAILLOW":(40,55,30,30,30,85),
    "SWELLOW":(60,85,60,50,50,125), "WINGULL":(40,30,30,55,30,85),
    "PELIPPER":(60,50,100,85,70,65), "RALTS":(28,25,25,45,35,40),
    "KIRLIA":(38,35,35,65,55,50), "GARDEVOIR":(68,65,65,125,115,80),
    "SURSKIT":(40,30,32,50,52,65), "MASQUERAIN":(70,60,62,80,82,60),
    "SHROOMISH":(60,40,60,40,60,35), "BRELOOM":(60,130,80,60,60,70),
    "SLAKOTH":(60,60,60,35,35,30), "VIGOROTH":(80,80,80,55,55,90),
    "SLAKING":(150,160,100,95,65,100), "NINCADA":(31,45,90,30,30,40),
    "NINJASK":(51,90,45,50,50,160), "SHEDINJA":(1,90,45,30,30,40),
    "WHISMUR":(64,51,23,51,23,28), "LOUDRED":(84,71,43,71,43,48),
    "EXPLOUD":(104,91,63,91,63,68), "MAKUHITA":(72,60,30,20,30,25),
    "HARIYAMA":(144,120,60,40,60,50), "AZURILL":(50,20,40,20,40,20),
    "NOSEPASS":(30,45,135,45,90,30), "SKITTY":(50,45,45,35,35,50),
    "DELCATTY":(70,65,65,55,55,70), "SABLEYE":(50,75,75,65,65,50),
    "MAWILE":(50,85,85,55,55,50), "ARON":(50,70,100,40,40,30),
    "LAIRON":(60,90,140,50,50,40), "AGGRON":(70,110,180,60,60,50),
    "MEDITITE":(30,40,55,40,55,60), "MEDICHAM":(60,60,75,60,75,80),
    "ELECTRIKE":(40,45,40,65,40,65), "MANECTRIC":(70,75,60,105,60,105),
    "PLUSLE":(60,50,40,85,75,95), "MINUN":(60,40,50,75,85,95),
    "VOLBEAT":(65,73,55,47,75,85), "ILLUMISE":(65,47,55,73,75,85),
    "ROSELIA":(50,60,45,100,80,65), "GULPIN":(70,43,53,43,53,40),
    "SWALOT":(100,73,83,73,83,55), "CARVANHA":(45,90,20,65,20,65),
    "SHARPEDO":(70,120,40,95,40,95), "WAILMER":(130,70,35,70,35,60),
    "WAILORD":(170,90,45,90,45,60), "NUMEL":(60,60,40,65,45,35),
    "CAMERUPT":(70,100,70,105,75,40), "TORKOAL":(70,85,140,85,70,20),
    "SPOINK":(60,25,35,70,80,60), "GRUMPIG":(80,45,65,90,110,80),
    "SPINDA":(60,60,60,60,60,60), "TRAPINCH":(45,100,45,45,45,10),
    "VIBRAVA":(50,70,50,50,50,70), "FLYGON":(80,100,80,80,80,100),
    "CACNEA":(50,85,40,85,40,35), "CACTURNE":(70,115,60,115,60,55),
    "SWABLU":(45,40,60,40,75,50), "ALTARIA":(75,70,90,70,105,80),
    "ZANGOOSE":(73,115,60,60,60,90), "SEVIPER":(73,100,60,100,60,65),
    "LUNATONE":(70,55,65,95,85,70), "SOLROCK":(70,95,85,55,65,70),
    "BARBOACH":(50,48,43,46,41,60), "WHISCASH":(110,78,73,76,71,60),
    "CORPHISH":(43,80,65,50,35,35), "CRAWDAUNT":(63,120,85,90,55,55),
    "BALTOY":(40,40,55,40,70,55), "CLAYDOL":(60,70,105,70,120,75),
    "LILEEP":(66,41,77,61,87,23), "CRADILY":(86,81,97,81,107,43),
    "ANORITH":(45,95,50,40,50,75), "ARMALDO":(75,125,100,70,80,45),
    "FEEBAS":(20,15,20,10,55,80), "MILOTIC":(95,60,79,100,125,81),
    "CASTFORM":(70,70,70,70,70,70), "KECLEON":(60,90,70,60,120,40),
    "SHUPPET":(44,75,35,63,33,45), "BANETTE":(64,115,65,83,63,65),
    "DUSKULL":(20,40,90,30,90,25), "DUSCLOPS":(40,70,130,60,130,25),
    "TROPIUS":(99,68,83,72,87,51), "CHIMECHO":(65,50,70,95,80,65),
    "ABSOL":(65,130,60,75,60,75), "WYNAUT":(95,23,48,23,48,23),
    "SNORUNT":(50,50,50,50,50,50), "GLALIE":(80,80,80,80,80,80),
    "SPHEAL":(70,40,50,55,50,25), "SEALEO":(90,60,70,75,70,45),
    "WALREIN":(110,80,90,95,90,65), "CLAMPERL":(35,64,85,74,55,32),
    "HUNTAIL":(55,104,105,94,75,52), "GOREBYSS":(55,84,105,114,75,52),
    "RELICANTH":(100,90,130,45,65,55), "LUVDISC":(43,30,55,40,65,97),
    "BAGON":(45,75,60,40,30,50), "SHELGON":(65,95,100,60,50,50),
    "SALAMENCE":(95,135,80,110,80,100), "BELDUM":(40,55,80,35,60,30),
    "METANG":(60,75,100,55,80,50), "METRAGROSS":(80,135,130,95,90,70),
    "REGIROCK":(80,100,200,50,100,50), "REGICE":(80,50,100,100,200,50),
    "REGISTELL":(80,75,150,75,150,50), "LATIAS":(80,80,90,110,130,110),
    "LATIOS":(80,90,80,130,110,110), "KYOGRE":(100,100,90,150,140,90),
    "GROUDON":(100,150,140,100,90,90), "RAYQUAZA":(105,150,90,150,90,95),
    "JIRACHI":(100,100,100,100,100,100), "DEOXYS":(50,150,50,150,50,150),
    "TURTWIG":(55,68,64,45,55,31), "GROTLE":(75,89,85,55,65,36),
    "TORTERRA":(95,109,105,75,85,56), "CHIMCHAR":(44,58,44,58,44,61),
    "MONFERNO":(64,78,52,78,52,81), "INFERNAPE":(76,104,71,104,71,108),
    "PIPLUP":(53,51,53,61,56,40), "PRINPLUP":(64,66,68,81,76,50),
    "EMPOLEON":(84,86,88,111,101,60), "STARLY":(40,55,30,30,30,60),
    "STARAVIA":(55,75,50,40,40,80), "STARAPTOR":(85,120,70,50,50,100),
    "BIDOOF":(59,45,40,35,40,31), "BIBAREL":(79,85,60,55,60,71),
    "KRICKETOT":(37,25,41,25,41,25), "KRICKETUNE":(77,85,51,55,51,65),
    "SHINX":(45,65,34,40,34,45), "LUXIO":(60,85,49,60,49,60),
    "LUXRAY":(80,120,79,95,79,70), "BUDEW":(40,30,35,50,70,55),
    "ROSERADE":(60,70,55,125,105,90), "CRANIDOS":(67,125,40,30,30,58),
    "RAMPARDOS":(97,165,60,65,50,58), "SHIELDON":(30,42,118,42,88,30),
    "BASTIODON":(60,52,168,47,138,30), "BURMY":(40,29,45,29,45,36),
    "WORMADAM":(60,59,85,79,105,36), "MOTHIM":(70,94,50,94,50,66),
    "COMBEE":(30,30,42,30,42,70), "VESPIQUEN":(70,80,102,80,102,40),
    "PACHIRISU":(60,45,70,45,90,95), "BUIZEL":(55,65,35,60,30,85),
    "FLOATZEL":(85,105,55,85,50,115), "CHERUBI":(45,35,45,62,53,35),
    "CHERRIM":(70,60,70,87,78,85), "SHELLOS":(76,48,48,57,62,34),
    "GASTRODON":(111,83,68,92,82,39), "AMBIPOM":(75,100,66,60,66,115),
    "DRIFLOON":(90,50,34,60,44,70), "DRIFBLIM":(150,80,44,90,54,80),
    "BUNEARY":(55,66,44,44,56,85), "LOPUNNY":(65,76,84,54,96,105),
    "MISMAGIUS":(60,60,60,105,105,105), "HONCHKROW":(100,125,52,105,52,71),
    "GLAMEOW":(49,55,42,42,37,85), "PURUGLY":(71,82,64,64,59,112),
    "CHINGLING":(45,30,50,65,50,45), "STUNKY":(63,63,47,41,41,74),
    "SKUNTANK":(103,93,67,71,61,84), "BRONZOR":(57,24,86,24,86,23),
    "BRONZONG":(67,89,116,79,116,33), "BONSLY":(50,80,95,10,45,10),
    "MIME,JR.":(20,25,45,70,90,60), "HAPPINY":(100,5,5,15,65,30),
    "CHATOT":(76,65,45,92,42,91), "SPIRITOMB":(50,92,108,92,108,35),
    "GIBLE":(58,70,45,40,45,42), "GABITE":(68,90,65,50,55,82),
    "GARCHOMP":(108,130,95,80,85,102), "MUNCHLAX":(135,85,40,40,85,5),
    "RIOLU":(40,70,40,35,40,60), "LUCARIO":(70,110,70,115,70,90),
    "HIPPOPOTAS":(68,72,78,38,42,32), "HIPPOWDON":(108,112,118,68,72,47),
    "SKORUPI":(40,50,90,30,55,65), "DRAPION":(70,90,110,60,75,95),
    "CROAGUNK":(48,61,40,61,40,50), "TOXICROAK":(83,106,65,86,65,85),
    "CARNIVINE":(74,100,72,90,72,46), "FINNEON":(49,49,56,49,61,66),
    "LUMINEON":(69,69,76,69,86,91), "MANTYKE":(45,20,50,60,120,50),
    "SNOVER":(60,62,50,62,60,40), "ABOMASNOW":(90,92,75,92,85,60),
    "WEAVILE":(70,120,65,45,85,125), "MAGNEZONE":(70,70,115,130,90,60),
    "LICKILICKY":(110,85,95,80,95,50), "RHYPERIOR":(115,140,130,55,55,40),
    "TANGROWTH":(100,100,125,110,50,50), "ELECTIVIRE":(75,123,67,95,85,95),
    "MAGMORTAR":(75,95,67,125,95,83), "TOGEKISS":(85,50,95,120,115,80),
    "YANMEGA":(86,76,86,116,56,95), "LEAFEON":(65,110,130,60,65,95),
    "GLACEON":(65,60,110,130,95,65), "GLISCOR":(75,95,125,45,75,95),
    "MAMOSWINE":(110,130,80,70,60,80), "PORYGON-Z":(85,80,70,135,75,90),
    "GALLADE":(68,125,65,65,115,80), "PROBOPASS":(60,55,145,75,150,40),
    "DUSKNOIR":(45,100,135,65,135,45), "FROSLASS":(70,80,70,80,70,110),
    "ROTOM":(50,50,77,95,77,91), "UXIE":(75,75,130,75,130,95),
    "MESPRIT":(80,105,105,105,105,80), "AZELF":(75,125,70,125,70,115),
    "DIALGA":(100,120,120,150,100,90), "PALKIA":(90,120,100,150,120,100),
    "HEATRAN":(91,90,106,130,106,77), "REGIGIGAS":(110,160,110,80,110,100),
    "GIRATINA":(150,100,120,100,120,90), "CRESSELIA":(120,70,120,75,130,85),
    "PHIONE":(80,80,80,80,80,80), "MANAPHY":(100,100,100,100,100,100),
    "DARKRAI":(70,90,90,135,90,125), "SHAYMIN":(100,100,100,100,100,100),
    "ARCEUS":(120,120,120,120,120,120), "VICTINI":(100,100,100,100,100,100),
    "SNIVY":(45,45,55,45,55,63), "SERVINE":(60,60,75,60,75,83),
    "SEPERIOR":(75,75,95,75,95,113), "TEPIG":(65,63,45,45,45,45),
    "PIGNITE":(90,93,55,70,55,55), "EMBOAR":(110,123,65,100,65,65),
    "OSHAWOTT":(55,55,45,63,45,45), "DEWOTT":(75,75,60,83,60,60),
    "SAMUROTT":(95,100,85,108,70,70), "PATRAT":(45,55,39,35,39,42),
    "WATCHOG":(60,85,69,60,69,77), "LILIPUP":(45,60,45,25,45,55),
    "HERDIER":(65,80,65,35,65,60), "STOUTLAND":(85,100,90,45,90,80),
    "PURRLOIN":(41,50,37,50,37,66), "LIEPARD":(64,88,50,88,50,106),
    "PANSAGE":(50,53,48,53,48,64), "SIMISAGE":(75,98,63,98,63,101),
    "PANSEAR":(50,53,48,53,48,64), "SIMISEAR":(75,98,63,98,63,101),
    "PANPOUR":(50,53,48,53,48,64), "SIMIPOUR":(75,98,63,98,63,101),
    "MUNNA":(76,25,45,67,55,24), "MUSHARNA":(116,55,85,107,95,29),
    "PIDOVE":(50,55,50,36,30,43), "TRANQUILL":(62,77,62,50,42,65),
    "UNFEZANT":(80,105,80,65,55,93), "BLITZLE":(45,60,32,50,32,76),
    "ZEBSTRIKA":(75,100,63,80,63,116), "ROGGENROLA":(55,75,85,25,25,15),
    "BOLDORE":(70,105,105,50,40,20), "GIGALITH":(85,135,130,60,70,25),
    "WOOBAT":(55,45,43,55,43,72), "SWOOBAT":(67,57,55,77,55,114),
    "DRILBUR":(60,85,40,30,45,68), "EXADRILL":(110,135,60,50,65,88),
    "AUDINO":(103,60,86,60,86,50), "TIMBURR":(75,80,55,25,35,35),
    "GURDURR":(85,105,85,40,50,40), "CONKELDURR":(105,140,95,55,65,45),
    "TYMPOLE":(50,50,40,50,40,64), "PALPITOAD":(75,65,55,65,55,69),
    "SEISMITOAD":(105,85,75,85,75,74), "THROH":(120,100,85,30,85,45),
    "SAWK":(75,125,75,30,75,85), "SEWADDLE":(45,53,70,40,60,42),
    "SWADLOON":(55,63,90,50,80,42), "LEAVANNY":(75,103,80,70,70,92),
    "VENIPEDE":(30,45,59,30,39,57), "WHIRLIPEDE":(40,55,99,40,79,47),
    "SCOLIPEDE":(60,90,89,55,69,112), "COTTONEE":(40,27,60,37,50,66),
    "WHIMSICOTT":(60,67,85,77,75,116), "PETILIL":(45,35,50,70,50,30),
    "LILLIGANT":(70,60,75,110,75,90), "BASCULIN":(70,92,65,80,55,98),
    "SANDILE":(50,72,35,35,35,65), "KROKOROK":(60,82,45,45,45,74),
    "KROOKODILE":(95,117,70,65,70,92), "DARUMAKA":(70,90,45,15,45,50),
    "DARMANITAN":(105,140,55,30,55,95), "MARACTUS":(75,86,67,106,67,60),
    "DWEBBLE":(50,65,85,35,35,55), "CRUSTLE":(70,95,125,65,75,45),
    "SCRAGGY":(50,75,70,35,70,48), "SCRAFTY":(65,90,115,45,115,58),
    "SIGILYPH":(72,58,80,103,80,97), "YAMASK":(38,30,85,55,65,30),
    "COFAGRIGUS":(58,50,145,95,105,30), "TIRTOUGA":(54,78,103,53,45,22),
    "CARRACOSTA":(74,108,133,83,65,32), "ARCHEN":(55,112,45,74,45,70),
    "ARCHEOPS":(75,140,65,112,65,110), "TRUBBISH":(50,50,62,40,62,65),
    "GARBODOR":(80,95,82,60,82,75), "ZORUA":(40,65,40,80,40,65),
    "ZOROARK":(60,105,60,120,60,105), "MINCCINO":(55,50,40,40,40,75),
    "CINCCINO":(75,95,60,65,60,115), "GOTHITA":(45,30,50,55,65,45),
    "GOTHORITA":(60,45,70,75,85,55), "GOTHITELLE":(70,55,95,95,110,65),
    "SOLOSIS":(45,30,40,105,50,20), "DUOSION":(65,40,50,125,60,30),
    "REUNICLUS":(110,65,75,125,85,30), "DUCKLETT":(62,44,50,44,50,55),
    "SWANNA":(75,87,63,87,63,98), "VANILLITE":(36,50,50,65,60,44),
    "VANILLISH":(51,65,65,80,75,59), "VANILLUXE":(71,95,85,110,95,79),
    "DEERLING":(60,60,50,40,50,75), "SAWSBUCK":(80,100,70,60,70,95),
    "EMOLGA":(55,75,60,75,60,103), "KARRABLAST":(50,75,45,40,45,60),
    "ESCAVALIER":(70,135,105,60,105,20), "FOONGUS":(69,55,45,55,55,15),
    "AMOONGUSS":(114,85,70,85,80,30), "FRILLISH":(55,40,50,65,85,40),
    "JELLICENT":(100,60,70,85,105,60), "ALOMOMOLA":(165,75,80,40,45,65),
    "JOLTIK":(50,47,50,57,50,65), "GALVANTULA":(70,77,60,97,60,108),
    "FERROSEED":(44,50,91,24,86,10), "FERROTHORN":(74,94,131,54,116,20),
    "KLINK":(40,55,70,45,60,30), "KLANG":(60,80,95,70,85,50),
    "KLINKLANG":(60,100,115,70,85,90), "TYNAMO":(35,55,40,45,40,60),
    "EELEKTRIK":(65,85,70,75,70,40), "EELEKTROSS":(85,115,80,105,80,50),
    "ELGYEM":(55,55,55,85,55,30), "BEHEEYEM":(75,75,75,125,95,40),
    "LITWICK":(50,30,55,65,55,20), "LAMPENT":(60,40,60,95,60,55),
    "CHANDELURE":(60,55,90,145,90,80), "AXEW":(46,87,60,30,40,57),
    "FRAXURE":(66,117,70,40,50,67), "HAXORUS":(76,147,90,60,70,97),
    "CUBCHOO":(55,70,40,60,40,40), "BEARTIC":(95,110,80,70,80,50),
    "CRYOGONAL":(70,50,30,95,135,105), "SHELMET":(50,40,85,40,65,25),
    "ACCELGOR":(80,70,40,100,60,145), "STUNFISK":(109,66,84,81,99,32),
    "MIENFOO":(45,85,50,55,50,65), "MIENSHAO":(65,125,60,95,60,105),
    "DRUDDIGON":(77,120,90,60,90,48), "GOLETT":(59,74,50,35,50,35),
    "GOLURK":(89,124,80,55,80,55), "PAWNIARD":(45,85,70,40,40,60),
    "BISHARP":(65,125,100,60,70,70), "BOUFFALANT":(95,110,95,40,95,55),
    "RUFFLET":(70,83,50,37,50,60), "BRAVIARY":(100,123,75,57,75,80),
    "VULLABY":(70,55,75,45,65,60), "MANDIBUZZ":(110,65,105,55,95,80),
    "HEATMOR":(85,97,66,105,66,65), "DURANT":(58,109,112,48,48,109),
    "DEINO":(52,65,50,45,50,38), "ZWEILOUS":(72,85,70,65,70,58),
    "HYDREIGON":(92,105,90,125,90,98), "LARVESTA":(55,85,55,50,55,60),
    "VOLCARONA":(85,60,65,135,105,100), "COBALION":(91,90,129,90,72,108),
    "TERRAKION":(91,129,90,72,90,108), "VIRIZION":(91,90,72,90,129,108),
    "TORNADUS":(79,115,70,125,80,111), "THUNDURUS":(79,115,70,125,80,111),
    "RESHIRAM":(100,120,100,150,120,90), "ZEKROM":(100,150,120,120,100,90),
    "LANDORUS":(89,125,90,115,80,101), "KYUREM":(125,130,90,130,90,95),
    "KELDEO":(91,72,90,129,90,108), "MELOETTA":(100,77,77,128,128,90),
    "GENESECT":(71,120,95,120,95,99) }

    wronginput = '» [WRONG INPUT] '
    examplestr = ' [EXAMPLE] '
    resultsestr = '» [RESULTS] '

############### start ###############
print('POKECALC by Space\n\nPlease enter the information requested below.')
start()
