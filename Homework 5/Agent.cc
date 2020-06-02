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
	//Initialize Map
	map[0][0] = 0;
	map[1][0] = 0;
	map[2][0] = 0;
	map[3][0] = 0;
	map[0][1] = 0;
	map[1][1] = 0;
	map[2][1] = 0;
	map[3][1] = 0;
	map[0][2] = 0;
	map[1][2] = 0;
	map[2][2] = 0;
	map[3][2] = 0;
	map[0][3] = 8;
	map[1][3] = 0;
	map[2][3] = 0;
	map[3][3] = 0;
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

Action Agent::TurnLeft ()
{
	setOrientation(getOrientation() - 3);
	if (getOrientation() < 3)
	{
		setOrientation(12);
	}
	return TURNLEFT;
}

Action Agent::TurnRight ()
{
        setOrientation(getOrientation() + 3);
        if (getOrientation() > 12)
        {
                setOrientation(3);
        }
        return TURNRIGHT;
}

Action Agent::GoForward ()
{
	if (getOrientation() == 12 && getY() < 4)
	{
		setY(getY()+1);
		return GOFORWARD;
	}
	else if (getOrientation() == 6 && getY() > 1)
	{
		setY(getY()-1);
		return GOFORWARD;
	}
	else if (getOrientation() == 3 && getX() < 4)
	{
		setX(getX()+1);
		return GOFORWARD;
	}
	else if (getOrientation() == 9 && getX() > 1)
	{
		setX(getX()-1);
		return GOFORWARD;
	}
	else
	{
		int random = rand() % 2 + 1;
		if (random == 1)
		{
			setmap(getX(), getY(), 8);
			return TurnLeft();
		}
		else
		{
			setmap(getX(), getY(), 8);
			return TurnRight();
		}

	}

}

int Agent::getmap (int x, int y)
{
        int a = 0;
        int b = 0;
        if (x == 1)
        {
                a = 0;
        }
        if (x == 2)
        {
                a = 1;
        }
        if (x == 3)
        {
                a = 2;
        }
        if (x == 4)
        {
                a = 3;
        }
        if (y == 1)
        {
                b = 3;
        }
        if (y == 2)
        {
                b = 2;
        }
        if (y == 3)
        {
                b = 1;
        }
        if (y == 4)
        {
                b = 0;
	}
	return map[a][b];
}

void Agent::setmap (int x, int y, int c)
{
	int a = 0;
	int b = 0;
	if (x == 1)
	{
		a = 0;
	}
	if (x == 2)
	{
		a = 1;
	}
	if (x == 3)
	{
		a = 2;
	}
	if (x == 4)
	{
		a = 3;
	}
	if (y == 1)
	{
		b = 3;
	}
	if (y == 2)
	{
		b = 2;
	}
	if (y == 3)
	{
		b = 1;
	}
	if (y == 4)
	{
		b = 0;
	}
	map[a][b] = c;
}

void Agent::printmap ()
{
	int i = 0;
	int j = 0;
	while (i < 4)
	{
		cout << "[ ";
		while (j < 4)
		{
			cout << map[j][i] << " ";
			j++;
		}
		j = 0;
		i++;
		cout << "]" << endl;
	}
	cout << getX() << ", " << getY() << endl;
	cout << getmap(getX(), getY()) << endl;
}

void Agent::safeupdate ()
{
	if (getOrientation() == 12 && getY() > 1)
	{
		setmap(getX(), getY() - 1, 8);
	}
	else if (getOrientation() == 6 && getY() < 4)
	{
		setmap(getX(), getY() + 1, 8);
	}
	else if (getOrientation() == 3 && getX() > 1)
	{
		setmap(getX() - 1, getY(), 8);
	}
	else if (getOrientation() == 6 && getX() < 4)
	{
		setmap(getX() + 1, getY(), 8);
	} 
}

void Agent::stenchupdate ()
{
	if (getmap(getX(), getY()) == 0)
	{
		if (getX() < 4)
		{
			if (getmap(getX() + 1, getY()) < 5)
			{
				setmap(getX() + 1, getY(), getmap(getX() + 1, getY()) + 1);
			}
		}
		if (getX() > 1)
		{
			if (getmap(getX() - 1, getY()) < 5)
			{
				setmap(getX() - 1, getY(), getmap(getX() - 1, getY()) + 1);
			}
		}
		if (getY() < 4)
		{
			if (getmap(getX(), getY() + 1) < 5)
			{
				setmap(getX(), getY() + 1, getmap(getX(), getY() + 1) + 1);
			}
		}
		if (getY() > 1)
		{
			if (getmap(getX(), getY() - 1) < 5)
			{
				setmap(getX(), getY() - 1, getmap(getX(), getY() - 1) + 1);
			}
		}
		setmap(getX(), getY(), 8);
	} 
}



Action Agent::Process (Percept& percept)
{
	srand (time(NULL));
	char c;
	Action action;
	bool validAction = false;
	//variable used in the bump percept
	int random = 0;
	printmap();

	while (! validAction)
	{
		validAction = true;
		if (percept.Glitter == 1) {
			action = GRAB;
			setGold(1);
                } else if (getX() == 1 && getY() == 1 && getGold() == 1) {
                        action = CLIMB;
		} else if (percept.Stench == 1 && getmap(getX(), getY()) == 0) {
			stenchupdate();
                } else{
			random = rand() % 10 + 1;
			if (random < 8)
			{
                        	action = GoForward();
				safeupdate();
			}
                	else if (random == 9)
                	{
                        	setmap(getX(), getY(), 8);
                        	return TurnLeft();
                	}
                	else
                	{
                        	setmap(getX(), getY(), 8);
                        	return TurnRight();
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

