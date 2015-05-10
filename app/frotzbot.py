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
        print( ">>> do_save: %s, overwrite=%d" % (filename,overwrite))
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

    def do_command( self, cmd, is_new=False ):
        self._last_command = cmd
        return super( ZorkWrapper, self ).do_command( cmd, is_new=is_new )

    HEADER = [
        "ZORK I: The Great Underground Empire",
        "Copyright (c) 1981, 1982, 1983 Infocom, Inc. All rights reserved.",
        "ZORK is a registered trademark of Infocom, Inc.",
        "Revision 88 / Serial number 840726"
    ]

    def process_output( self, output, is_new=False ):
        print "process_output. is_new=%d" % is_new
        lines = output.split("\n")
        buf = []
        for line in lines:
            do_append = True
            line = line.rstrip()
            if is_new and (line in ZorkWrapper.HEADER):
                do_append = False
            elif len(line) < 1:
                do_append = False
            elif line.startswith(self._last_command):
                do_append = False
            if do_append:
                buf.append( line )
        return "\n".join(buf)


if __name__ == '__main__':
    # Set these to something sensible
    frotz_binary =  os.path.expanduser( "frotz/dfrotz" )
    story_file = os.path.expanduser( "~/DATA/ZORK1.DAT" )

    w = ZorkWrapper( frotz_binary, story_file )

    fn_state = sys.argv[1]

    cmd = "look"
    is_new = True

    if os.path.exists( fn_state ):
        print ">>> load state"
        w.load( fn_state )
        cmd = " ".join( sys.argv[2:] )
        is_new = False
    
    print ">>> do command IN"
    print w.do_command( cmd, is_new=is_new )
    print ">>> do command OUT"
    w.save_quit( fn_state, overwrite=(not is_new) )


    