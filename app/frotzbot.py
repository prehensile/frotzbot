#!/usr/bin/env python
import pexpect
import os, sys

class FrotzWrapper( object ):

    # Hackity hack hack hack:  need to make this less fragile!
    PROMPTS = ["\n>", "\n> >","to begin]", "\n\*\*\*MORE\*\*\*"]

    def __init__( self, frotz_binary, story_file ):
        self._frotz = self.start_frotz( frotz_binary, story_file )

    def start_frotz( self, frotz_binary, story_file ):    
        cmd = "%s %s" % ( frotz_binary, story_file )
        return pexpect.spawn( cmd )

    def process_output( self, output, is_new=False ):
        # extend in subclass
        return output

    def do_command( self, cmd, is_new=False ):
        self._frotz.sendline( cmd )
        self._frotz.expect( FrotzWrapper.PROMPTS )
        return self.process_output( self._frotz.before, is_new=is_new )

    def do_save( self, filename, overwrite=False ):
        self._frotz.sendline( "save" )
        self._frotz.expect( ":" )
        self._frotz.sendline( filename )
        if overwrite:
            self._frotz.expect( ".*Overwrite existing file.*" )
            self._frotz.sendline( "y" )
        self._frotz.expect( FrotzWrapper.PROMPTS )

    def save_quit( self, filename, overwrite=False ):
        self.do_save( filename, overwrite )
        self._frotz.sendline( "quit" )
        self._frotz.expect( ".*Do you wish to leave the game.*" )
        self._frotz.sendline( "Y" )

    def load( self, filename ):
        self._frotz.expect( FrotzWrapper.PROMPTS )
        self._frotz.sendline( "restore" )
        self._frotz.expect( ":" )
        self._frotz.sendline( filename )
        self._frotz.expect( FrotzWrapper.PROMPTS )

class ZorkWrapper( FrotzWrapper ):

    HEADER = [
        "ZORK I: The Great Underground Empire",
        "Copyright (c) 1981, 1982, 1983 Infocom, Inc. All rights reserved.",
        "ZORK is a registered trademark of Infocom, Inc.",
        "Revision 88 / Serial number 840726"
    ]

    def process_output( self, output, is_new=False ):
        lines = output.split("\n")[1:]
        buf = []
        for line in lines:
            do_append = True
            line = line.rstrip()
            if is_new and (line in ZorkWrapper.HEADER):
                do_append = False
            elif len(line) < 1:
                do_append = False
            if do_append:
                buf.append( line )
        return "\n".join(buf)


class ZorkBot( object ):

    def __init__( self, frotz_binary=None, story_file=None, save_path=None ):
        self._frotz_binary = frotz_binary
        self._story_file = story_file
        self._save_path = save_path

    def command_for_user( self, command=None, username=None ):
        w = ZorkWrapper( self._frotz_binary, self._story_file )
        fn_state = os.path.join( self._save_path, username )
        
        is_new = True

        if os.path.exists( fn_state ):
            w.load( fn_state )
            is_new = False
        
        s = w.do_command( command, is_new=is_new )
        w.save_quit( fn_state, overwrite=(not is_new) )
        return s

    def generate( self ):
        return None

    def reply( self, tweet=None, to_username=None, to_userid=None ):
        body = self.command_for_user( command=tweet, username=to_userid )
        return body


# commandline testing stub
if __name__ == '__main__':
    
    frotz_binary = "frotz/dfrotz"
    story_file = "stories/zork1.dat"
    save_path = "saves"
    
    fn_state = sys.argv[1]
    cmd = " ".join( sys.argv[2:] )

    b = ZorkBot( frotz_binary=frotz_binary, story_file=story_file, save_path=save_path )
    print b.command_for_user( cmd, fn_state )


    


    