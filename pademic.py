"""
This is the simulation of a pandemic with a 2D visualization to help the comprehension.
Developed by Mattia Neroni the 13th October 2020.
"""

import pygame # type: ignore
import pygame.freetype # type: ignore
import random

from collections import namedtuple
from dataclasses import dataclass



Size = namedtuple("Size", "x y")
Position = namedtuple("Position", "x y")




class WINDOW (object):
    """
    This class is an interface containing the global variables for the Window.
    :class_attr black: The color black in RGB
    :class_attr white: The color white in RGB
    :class_attr red: The color red in RGB
    :class_attr green: The color green in RGB
    :class_attr blue: The color blue in RGB
    :class_attr size: The size of the window used in the visual simulation.
    :class_attr person_size: The size of an individual in the visual simulation.
    :class_attr clocktick: The clock tick in the visual simulation.
    """
    black = (0 , 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

    person_size = Size (x=3, y=3)
    clocktick = 20




class STATE:
	"""
	This class in an interface containing the possible states in which
	a person can be found.
	"""
	ill : str = "ILL"
	healty : str = "HEALTY"
	latent :str = "LATENT"







@dataclass
class Virus:
	"""
	This class represents the virus spreading during the pandemic.
	:attr chance: The chance to infect a healty person after a contact.
	:attr distance: The minumum distance necessary to have an infection.
	:attr latency: The time from the infection to the first symptoms.
	:attr illness: The time from the first symptoms to the healing.
	:attr immunity: The duration of the immunity (if infinite use float("inf")).
	"""
	chance : float
	distance : int
	latency : int
	illness : int
	immunity : float









class Person (pygame.sprite.Sprite):
    """
    Class to represent a person.
    """
    def __init__ (self, position):
        """
        Initialize
	
	:param position: Her/his strating position.
	
        """
        super().__init__()

        # Set height, width
        self.image = pygame.Surface (WINDOW.person_size)
        self.image.fill (WINDOW.green)
        
        # Set the position
        self.rect = self.image.get_rect()
        self.rect.x = position.x
        self.rect.y = position.y

        self.position = position
        self.state = STATE.healty
        self.history = []






    def set_pos (self, position):
        """
        This method sets a new position for the person involved.
        """
        self.position = position
        self.rect.x = position.x
        self.rect.y = position.y






    def immune (self, time):
    	"""
		This method checks in a given instant of the simulation if the person
		is immune or not.
		:param time: <int> The current simulation time.
		:return: <bool> True if the person is immune, False otherwise.
    	"""
    	if len (self.history) > 0 and self.history[-1].get("get_healty"):
    		if self.history[-1].get("immunity") > time - self.history[-1].get("get_healty"):
    			return True
    	return False






    def set_state (self, time, state, virus):
        """
        This method change the state of a person and register when the change
        toke place.
	
	:param time: <int> The current simulation time.
	:param state: <str> The new state of th person.
	:param virus: <Virus> The virus that infected the person.
	
        """
        self.state = state

        if state == STATE.latent:
        	self.image.fill (WINDOW.blue)
        	self.history.append ({"get_latent" : time, "latency" : int(random.lognormvariate (virus.latency, virus.latency * 0.25))})

        elif state == STATE.ill:
        	self.image.fill (WINDOW.red)
        	self.history[-1]["get_ill"] = time
        	self.history[-1]["illness"] = int(random.lognormvariate (virus.illness, virus.illness * 0.25))

        elif state == STATE.healty:
        	self.image.fill (WINDOW.green)
        	self.history[-1]["get_healty"] = time
        	self.history[-1]["immunity"] = int(random.lognormvariate (virus.immunity, virus.immunity * 0.25))






    def upgrade_state (self, time):
    	"""
		This method upgrade the state of the person depending on the time
		passed after the last change of state.
		Finally, it returns the new state of the person.
		
		:param time: <int> The current simulation time.
		:return: <str> The new state of the person.
    	"""
    	if len(self.history) > 0:
    		if self.state == STATE.latent and time - self.history[-1]["get_latent"] >= self.history[-1]["latency"]:
    			return STATE.ill
    			
    		elif self.state == STATE.ill and time - self.history[-1]["get_ill"] >= self.history[-1]["illness"]:
    			return STATE.healty

    	return self.state












class Pandemic (object):
    """
    This is the main class representing the simulation of the pandemic.
    """

    def __init__ (self, population, init_ill, virus, quarantine, area):
        """
        Initialize.
        :attr population: <int> The total number of people
        :attr inti_ill: <int> The starting number of ill people
        :attr virus: <Virus> The characteristics of the virus
        :attr quarantine: <bool> If true the healing people are isolated and not contagious,
                            otherwise they go on infecting other people.
        :attr area: <Size> The size of the area where the people move
        """
        self.quarantine = quarantine
        self.area_size = area
        self.virus = virus

        self.population = {
            "healty" : [Person (Position (x=random.randint(0, area.x), y=random.randint(0, area.y))) for _ in range(population)],
            "latent" : [],
            "ill" : []
        }

        # Make some random people ill
        for _ in range (init_ill):
            p = self.population.get("healty").pop(random.randint(0, len(self.population.get("healty"))-1))
            p.set_state (0, STATE.latent, virus)
            self.population["latent"].append (p)





    @staticmethod
    def euclidean (pos1, pos2):
    	"""
		This method returns the euclidean distance between two positions.
		
		:param pos1: <Position> First position.
		:param pos2: <Position> Second position.
		:return: <int> The euclidean distance.
    	"""
    	return int(((pos1.x - pos2.x)**2 + (pos1.y - pos2.y)**2)**0.5)





    def contact (self, time,  contagious, healty):
        """
        This method represents a contact between a contagius and a healty person.
        It return True is the healty person is infected, and False otherwise.
        The infection depends on the chance of infection related to the virus.
	
	:param time: <int> The instant when the contact take place.
        :param contagious: <Person> The contagius person.
        :param healty: <Person> The healty person.
        :return: <bool> True if there is an infection, False otherwise.
	
        """
        rnd = random.random()

        if rnd < self.virus.chance:

            healty.set_state (time, STATE.latent, self.virus)
            self.population.get("healty").remove(healty)
            self.population["latent"].append(healty)

            return True

        return False






    def run (self, until):
    	"""
		This is the main method that runs the simulation.
    	"""
    	pygame.init()
    	screen = pygame.display.set_mode((self.area_size.x, self.area_size.y))
    	pygame.display.set_caption('Pandemic')

    	sprites = pygame.sprite.Group()
    	for p in self.population.get("healty") + self.population.get("latent") + self.population.get("ill"):
    		sprites.add (p)

    	clock = pygame.time.Clock()

    	time, done = 0, False
    	while time < until and done is False:
    		for event in pygame.event.get():
    			if event.type == pygame.QUIT:
    				done = True

    		time += 1
    		infection : bool

    		# Each person moves and eventually change state
    		for p in self.population.get("healty") + self.population.get("latent") + self.population.get("ill"):

    			new_state = p.upgrade_state (time)
    			if new_state != p.state:
    				p.set_state (time, new_state, self.virus)
    				if new_state == STATE.healty:
    					self.population.get("ill").remove(p)
    					self.population["healty"].append(p)
    				elif new_state == STATE.ill:
    					self.population.get("latent").remove(p)
    					self.population["ill"].append(p)


    			if not self.quarantine or (self.quarantine and p.state != STATE.ill):
    				p.set_pos (Position (x=p.position.x + random.choice([-1, 0, +1]), y=p.position.y + random.choice([-1, 0, +1])))

    		



    		# Infections
    		for healty in self.population.get("healty"):

    			if healty.immune(time) is False:

	    			infection = False

	    			for contagious in self.population.get("latent"):
	    				if self.euclidean (contagious.position, healty.position) < self.virus.distance:
	    					infection = self.contact (time, contagious, healty)
	    					if infection is True:
	    						break

	    			if self.quarantine is False and infection is False:
	    				for contagious in self.population.get("ill"):
	    					if self.euclidean (contagious.position, healty.position) < self.virus.distance:
	    						infection = self.contact (time, contagious, healty)
	    						if infection is True:
	    							break

	    	if time % 100 == 0:
	    		print (f"Infected : {len(self.population.get('ill'))}, Asymptomatic : {len(self.population.get('latent'))}, Healty : {len(self.population.get('healty'))} ")

    		screen.fill(WINDOW.black)
    		sprites.draw(screen)
    		pygame.display.flip()
    		clock.tick(WINDOW.clocktick)

    	pygame.quit()


if __name__ == "__main__":
 	v = Virus (chance=0.9, distance=4, latency=7, illness=30, immunity=float("inf"))
	p = Pandemic (population=1000, init_ill=30, virus=v, quarantine=False, area=Size(x=800, y=600))
	p.run (until=2000)
