// Agent.h

#ifndef AGENT_H
#define AGENT_H

#include "Action.h"
#include "Percept.h"

class Agent
{
public:
	Agent ();
	~Agent ();
	void Initialize ();
	Action Process (Percept& percept);
	void GameOver (int score);

	//Getters and Setters to access Agent information
	void setOrientation(int orientation);
	int getOrientation ();
	void setGold(int gold);
	int getGold ();
	void setArrow(int arrow);
	int getArrow ();
	void setY(int y);
	int getY ();
	void setX(int x);
	int getX ();

private:
	//Orientations are 12, 3, 6, and 9. Up, right, down, left respectively like on a clock
	int Orientation;

	//1 if gold is held, 0 otherwise
	int Gold;

	//1 if Arrow is held, 0 otherwise
	int Arrow;

	//Coordinates so the Agent knows when its at [1, 1]
	int X;
	int Y;
};

#endif // AGENT_H
