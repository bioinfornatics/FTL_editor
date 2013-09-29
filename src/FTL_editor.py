#!/usr/bin/env python3


from sys        import argv
from argparse   import ArgumentParser
from os.path    import expanduser
from struct     import unpack, pack

BYTE_SHIFT  = 4
POS         = 0
FIELD       = 0
DATA_TYPE   = [
                    'int_list',     # unknown
                    'int_list',     # unknown
                    'int',          # unknown
                    'string',       # ship name
                    'string',       # ship amelioration ?
                    'int_list',     # unknown
                    'int',          # unknown
                    'string',       # ship amelioration
                    'string',       # ship name
                    'string',       # ship sub name
                    'crew_list'     # crew list
                ]
                #'int',         # health
                #'int',         # fuel
                #'int',         # missile
                #'int'          # scrap
         
SAVEFILE    = expanduser( '~/.local/share/FasterThanLight/continue.sav' )
SAVEGAME    = open( SAVEFILE, 'rb' ).read()
       
def byte_to_int():
    global POS
    global BYTE_SHIFT
    value   = int( unpack( '1i', SAVEGAME[POS:POS+BYTE_SHIFT] )[0] )
    POS     += BYTE_SHIFT
    return value

def byte_to_string():
    global POS
    global BYTE_SHIFT
    global SAVEGAME
    length  = byte_to_int()
    start   = POS
    end     = POS + length
    POS     = end
    return str( unpack( str(length) + 's', SAVEGAME[start:end] )[0], 'ascii' )
    
def menu():
    print( '---------------------------------')
    print( '1/ Set Health' )
    print( '2/ Set Fuel' )
    print( '3/ Set number of drones' )
    print( '4/ Set number of missiles' )
    print( '5/ Set number of Scrap' )
    print( '6/ Exit' )
    print( '---------------------------------')
    
    first       = 1
    last        = 6
    choice      = None
    isAsking    = True
    
    while isAsking:
        try:
            choice = int( input( 'choice: ' ) )
        except ValueError:
            print( 'You need to put a number between {} - {} !'.format(first, last) )
        if choice is not None:
            if choice < first or choice > last:
                choice = None
                print( 'You need to put a number between {} - {} !'.format(first, last) )
            else:
                isAsking = False
    return choice

if __name__ == '__main__':

    data        = []
    isReading   = True

    while isReading:
        if FIELD >= len( DATA_TYPE ):
            isReading = False
        elif POS >= len( SAVEGAME ): 
            raise Exception( 'Reach too early end of file' )
        else:
            if DATA_TYPE[FIELD] == 'int_list':
                number_of_field = byte_to_int()
                for n in range(0, number_of_field ):
                    number = byte_to_int()
            elif DATA_TYPE[FIELD] == 'int':
                number  = byte_to_int()
            elif DATA_TYPE[FIELD] == 'string':
                word    = byte_to_string()
            elif DATA_TYPE[FIELD] == 'string_list':
                number_of_field = byte_to_int()
                for w in range(0, number_of_field ):
                    word    = byte_to_string()
            elif DATA_TYPE[FIELD] == 'crew_list':
                number_of_field = byte_to_int()
                for w in range(0, number_of_field ):
                    race    = byte_to_string()
                    name    = byte_to_string()
            else:
                raise Exception( 'Unknow data type: ' + DATA_TYPE[FIELD])
            
            FIELD   += 1

    save_pos1   = POS
    health      = byte_to_int()
    fuel        = byte_to_int()
    drone       = byte_to_int()
    missile     = byte_to_int()
    scrap       = byte_to_int()
    save_pos2   = POS
    
    choice      = 0
    
    
    if len( argv ) > 1:
        parser = ArgumentParser(description='Edit FTL savegame file.')
        parser.add_argument('-l', '--life'      , type = int, default = health  , help = 'Set amount of ship life' )
        parser.add_argument('-f', '--fuel'      , type = int, default = fuel    , help = 'Set amount of ship fuel' )
        parser.add_argument('-d', '--drone'     , type = int, default = drone   , help = 'Set amount of drone' )
        parser.add_argument('-m', '--missile'   , type = int, default = missile , help = 'Set amount of missile' )
        parser.add_argument('-s', '--scrap'     , type = int, default = scrap   , help = 'Set amount of scrap' )
        
        args = parser.parse_args()
        
        health      = args.life
        fuel        = args.fuel
        drone       = args.drone
        missile     = args.missile
        scrap       = args.scrap
        
        print( 'Current health: {}'.format( health ) )
        print( 'Current fuel: {}'.format( fuel ) )
        print( 'Current drone: {}'.format( drone ) )
        print( 'Current missile: {}'.format( missile ) )
        print( 'Current scrap: {}'.format( scrap ) )
    else:
        while choice != 6:
            print( 'Current health: {}'.format( health ) )
            print( 'Current fuel: {}'.format( fuel ) )
            print( 'Current drone: {}'.format( drone ) )
            print( 'Current missile: {}'.format( missile ) )
            print( 'Current scrap: {}'.format( scrap ) )
            
            choice = menu()
            
            if choice == 1:
                print( 'Current health: {}'.format( health ) )
                health = int( input( 'health: ' ) )
            elif choice == 2:
                print( 'Current fuel: {}'.format( fuel ) )
                fuel = int( input( 'fuel: ' ) )
            elif choice == 3:
                print( 'Current drone: {}'.format( drone ) )
                drone = int( input( 'drone: ' ) )
            elif choice == 4:
                print( 'Current missile: {}'.format( missile ) )
                missile = int( input( 'missile: ' ) )
            elif choice == 5:
                print( 'Current scrap: {}'.format( scrap ) )
                scrap = int( input( 'scrap: ' ) )
    
    SAVEGAME    = SAVEGAME[:save_pos1] + pack( 'i', health ) + pack( 'i', fuel ) + pack( 'i', drone ) + pack( 'i', missile ) + pack( 'i', scrap ) + SAVEGAME[save_pos2:]
    open( SAVEFILE, 'wb' ).write(SAVEGAME)
