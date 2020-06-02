// Agent.cc

#include <iostream>
#include "Agent.h"
#include <stdlib.h>
using namespace std;

Agent::Agent ()
{

}

Agent::~Agent ()
{

}

void Agent::Initialize ()
{
	Orientation = 3;
	Gold = 0;
	Arrow = 1;
	X = 1;
	Y = 1;
}

void Agent::setOrientation(int orientation)
{
	Orientation = orientation;
}

int Agent::getOrientation ()
{
	return Orientation;
}

void Agent::setGold(int gold)
{
	Gold = gold;
}

int Agent::getGold ()
{
	return Gold;
}

void Agent::setArrow(int arrow)
{
	Arrow = arrow;
}

int Agent::getArrow ()
{
	return Arrow;
}

void Agent::setY(int y)
{
	Y = y;
}

int Agent::getY ()
{
	return Y;
}

void Agent::setX(int x)
{
	X = x;
}

int Agent::getX ()
{
	return X;
}

Action Agent::Process (Percept& percept)
{
	srand (time(NULL));
	char c;
	Action action;
	bool validAction = false;
	//variable used in the bump percept
	int random = 0;

	while (! validAction)
	{
		validAction = true;
		if (percept.Glitter == 1) {
			action = GRAB;
			setGold(1);
                } else if (getX() == 1 && getY() == 1 && getGold() == 1) {
                        action = CLIMB;
		} else if (percept.Stench == 1 && getArrow() == 1) {
			action = SHOOT;
			setArrow(0);
		} else if (percept.Bump == 1) {
        		random = rand() % 2 + 1;
			if (random == 1)
			{
				action = TURNLEFT;
                        	setOrientation(getOrientation() - 3);
                        	if (getOrientation() < 3)
                        	{
                                	setOrientation(12);
                        	}
			}
			else
			{
				action = TURNRIGHT;
                        	setOrientation(getOrientation() + 3);
                        	if (getOrientation() > 12)
                        	{
                                	setOrientation(3);
                        	}

			}
                } else{
                        action = GOFORWARD;
			if (getOrientation() == 12)
			{
				setY(getY()+1);
			}
			else if (getOrientation() == 6)
			{
				setY(getY()-1);
			}
			else if (getOrientation() == 3)
			{
				setX(getX()+1);
			}
			else if (getOrientation() == 9)
			{
				setX(getX()-1);
			}
			if (getX() > 4)
			{
				setX(4);
			}
			if (getY() > 4)
			{
				setY(4);
			}
			if (getX() < 1)
			{
				setX(1);
			}
			if (getY() < 1)
			{
				setY(1);
			}
		}
	}
	cout << "Location: [" << getX() << ", " << getY() << "]" << endl;
	cout << "Orientation: " << getOrientation() << endl;
	cout << "Gold: " << getGold() << endl;
	cout << "Arrow: " << getArrow() << endl;
	return action;
}

void Agent::GameOver (int score)
{

}

