import doctest
from note import Note
class Melody:
    '''
    Stores information about a melody of many notes, and
    operations to perform on them.
    Attributes: title, author, notes
    '''
    def __init__(self, filename):
        '''
        (str) -> Nonetype
        open the file, create an instance attribute for the title and author, then
        create an instance attribute called notes for a list that contains a sequence
        of Note objects, one for every note in the file 
        
        >>> hot_cross_buns = Melody("hotcrossbuns.txt")
        >>> len(hot_cross_buns.notes)
        17
        >>> print(hot_cross_buns.notes[10])
        0.25 A 4 natural
        
        >>> fur_elise = Melody("fur_elise.txt")
        >>> len(fur_elise.notes)
        165
        >>> print(fur_elise.notes[0])
        0.15 E 5 natural
        
        >>> twinkle = Melody("twinkle.txt")
        >>> len(twinkle.notes)
        42
        >>> print(twinkle.notes[5])
        0.5 A 4 natural
        '''
        fobj=open(filename)
        file_content = fobj.read()
        main=file_content.split('\n')
        self.title= main[0]
        self.author= main[1]
        
        notes=main[2:]
        ind_elmts=[]
        for note in notes:

            ind_elmts.append(note.split(' '))
        
        notes_list=[]
        indices=[]   
        
        for i in range(len(ind_elmts)):
            notes_list.append(ind_elmts[i])
            if ind_elmts[i][-1]=='true':
                indices.append(i)
                while len(indices)>=2:
                    first=indices[0]
                    last=indices[1]
                    
                    for el in ind_elmts[first:last+1]:
                            
                        notes_list.append(el)
                        
                    indices.remove(first)
                    indices.remove(last)  
              
        new=[]
        for elmt in notes_list:
            if elmt[1]=='R':
                note=Note(float(elmt[0]),elmt[1])
                
            else:
                note=Note(float(elmt[0]),elmt[1],int(elmt[2]),elmt[3])
            new.append(note)
        
        self.notes=new
    
        fobj.close()
        
    def play(self, m_player):
        '''
        (Player) -> Nonetype
        Calls the play method on each Note object of the notes instance attribute in order.
        '''
        for note in self.notes:
            note.play(m_player)
            
    def get_total_duration(self):
        '''
        () -> float
        Returns the total duration of the song as a float.
        
        >>> happy_birthday = Melody("birthday.txt")
        >>> happy_birthday.get_total_duration()
        13.0
        >>> fur_elise = Melody("fur_elise.txt")
        >>> fur_elise.get_total_duration()
        25.799999999999944
        
        >>> twinkle = Melody("twinkle.txt")
        >>> twinkle.get_total_duration()
        24.5
        
        '''
        duration=0
        for note in self.notes:
            duration+=note.duration
        return duration
    
    def lower_octave(self):
        '''
        () -> bool
        Reduces the octave of all notes in the song by 1 and returns True.
        However, if a note’s octave is 1 or below, then return False.
        
        >>> happy_birthday = Melody("birthday.txt")
        >>> happy_birthday.lower_octave()
        True
        >>> happy_birthday.notes[5].octave
        3
        
        >>> twinkle=Melody('twinkle.txt')
        >>> twinkle.notes[2].octave
        4
        >>> twinkle.notes[5].octave
        4
        >>> twinkle.lower_octave()
        True
        >>> twinkle.notes[2].octave
        3
        >>> twinkle.notes[5].octave
        3
        
        >>> furelise=Melody('fur_elise.txt')
        >>> furelise.notes[0].octave
        5
        >>> furelise.notes[5].octave
        4
        >>> furelise.lower_octave()
        True
        >>> furelise.notes[2].octave
        4
        >>> furelise.notes[5].octave
        3
        
        '''
        for note in self.notes:
            if note.pitch=='R':
                continue
            elif note.octave <= Note.OCTAVE_MIN or note.octave>= Note.OCTAVE_MAX:
                return False
            else:
                note.octave-=1
        return True
    def upper_octave(self):
        '''
        () -> bool
        It increases the octave of all notes in the song by 1 and returns True.
        However, a note’s octave cannot be increased past 7. If that would happen,
        then do not increase any octaves and instead return False.
        
        >>> happy_birthday = Melody("birthday.txt")
        >>> happy_birthday.upper_octave()
        True
        >>> happy_birthday.notes[5].octave
        5
        
        >>> twinkle=Melody('twinkle.txt')
        >>> twinkle.notes[2].octave
        4
        >>> twinkle.notes[5].octave
        4
        >>> twinkle.upper_octave()
        True
        >>> twinkle.notes[2].octave
        5
        >>> twinkle.notes[5].octave
        5
        
        >>> furelise=Melody('fur_elise.txt')
        >>> furelise.notes[0].octave
        5
        >>> furelise.notes[5].octave
        4
        >>> furelise.upper_octave()
        True
        >>> furelise.notes[2].octave
        6
        >>> furelise.notes[5].octave
        5
        '''
        for note in self.notes:
            if note.pitch=='R':
                continue
            elif note.octave <= Note.OCTAVE_MIN or note.octave >= Note.OCTAVE_MAX:
                return False
            else:
                note.octave+=1
        return True
    def change_tempo(self, pos_float):
        '''
        (float) -> Nonetype
        Multiplies the duration of each note by the given float.
        >>> happy_birthday = Melody("birthday.txt")
        >>> happy_birthday.change_tempo(0.5)
        >>> happy_birthday.get_total_duration()
        6.5
        >>> happy_birthday = Melody("birthday.txt")
        >>> happy_birthday.change_tempo(0)
        Traceback (most recent call last):
        AssertionError: Not positive float
        
        >>> fur_elise = Melody("fur_elise.txt")
        >>> fur_elise.get_total_duration()
        25.799999999999944
        >>> fur_elise.change_tempo(2)
        >>> fur_elise.get_total_duration()
        51.59999999999989
        '''
        if pos_float>0:
            for note in self.notes:
                note.duration*=pos_float
        else:
            raise AssertionError('Not positive float')
            

