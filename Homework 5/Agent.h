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

	//Turns and Moves
	Action TurnLeft ();
	Action TurnRight ();
	Action GoForward ();

	//Map updates
	int getmap (int x, int y);
	void setmap (int x, int y, int c);
	void printmap ();
	void safeupdate ();
	void stenchupdate ();

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

	//Safety Map
	//0 = Unknown, 5 = Wumpus, 8 = Safe/Visited, 1, 2, 3 = Hazardous level
	int map[4][4];  
};

#endif // AGENT_H
