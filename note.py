import doctest
import musicalbeeps


class Note:
    '''
    A class that represents a note.
    Attributes: OCTAVE_MIN, OCTAVE_MAX, duration, pitch, octave, accidental
    '''
    
    OCTAVE_MIN = 1
    OCTAVE_MAX = 7
    
    def __init__(self, duration, pitch, octave=1, accidental='natural'):
        '''(float,str,int,str)-> Nonetype
        Creates an object of type Note.
        >>> note = Note(2.0, "B", 4, "natural")
        >>> note.pitch
        'B'
        
        >>> note = Note(2.0, "R")
        >>> note.octave
        1
        
        >>> note = Note(2, "C",3,'sharp')
        Traceback (most recent call last):
        AssertionError: duration must be a float
        
        '''
        
        PITCH_CHAR='A,B,C,D,E,F,G,R'
        if type(duration)!=float or duration<=0:
            raise AssertionError('duration must be a positive float.')
        elif type(pitch)!=str or pitch not in PITCH_CHAR:
            raise AssertionError('pitch is not in correct format')
        elif type(octave)!=int or octave not in range(1,8):
            raise AssertionError('octave is not in correct format')
        elif type(accidental)!=str or accidental.lower() not in ["natural", "sharp", "flat"]:
            raise AssertionError('accidental is not in correct format')
    
        self.duration = duration
        self.pitch = pitch
        self.octave = octave
        self.accidental = accidental.lower()
    def __str__(self):
         '''() -> str
         returns a string of the format 'DURATION PITCH OCTAVE ACCIDENTAL' where
         each of the four words refer to the appropriate instance attributes.
        
         >>> note = Note(2.0, "B", 4, "NATURAL")
         >>> print(note)
         2.0 B 4 natural
         
         >>> rest = Note(2.0, "R")
         >>> print(rest)
         2.0 R 1 natural
         
         >>> inv = Note(2.0, "Z", 4,'natural')
         Traceback (most recent call last):
         AssertionError: pitch is not in correct format
         '''
         return str(self.duration)+' '+ self.pitch + ' '+ str(self.octave) + ' '+ self.accidental.lower()
            
    def play(self, player):
        '''
        (Player) -> Nonetype
        Constructs the note string that the play_note method accepts, then passes
        the note string and duration to it so that the note can be played through the
        speakers.
        '''
        if self.pitch =='R':
            target_note= 'pause'
        elif self.accidental=='sharp':
            target_note= self.pitch + str(self.octave) +'#'
        elif self.accidental=='flat':
            target_note= self.pitch + str(self.octave) +'b'
        else:
            target_note= self.pitch + str(self.octave)
        player.play_note(target_note, self.duration)

              