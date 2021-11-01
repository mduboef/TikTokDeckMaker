#include <iostream>
#include <string>

class Video{
public:
    // default constructor
    Video();

    // constructor
    Video(std::string nameIn, double spendIn, int typeIn, int viewsIn, int commentsIn, int likesIn, int sharesIn){
        name = nameIn;
        spend = spendIn;
        type = typeIn;
        views = viewsIn;
        comments = commentsIn;
        likes = likesIn;
        shares = sharesIn;
    }

    // getters
    std::string getName(){ return name; }

private:
    std::string name;
    double spend;
    int type;              // 0 boost, 1 product, 2 followers
    int views;
    int comments;
    int likes;
    int shares;
};