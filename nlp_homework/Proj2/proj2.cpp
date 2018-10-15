/* 
 * 分词系统
 * 字典:ce.txt
*/

#include<iostream>
#include<vector>

using namespace std;

class Dict{
    public:
        Dict();
        Dict(string filename);
        bool isInDict(string s);
        void setDict(string filename);
        ~Dict();
    private:
        long dict_size;
        vector<string> dict;
        string filename;
};

Dict::Dict(string filename){
    this->filename = filename;
    setDict(filename);
}

bool Dict::isInDict(string s){
    
}

void Dict::setDict(string filename){

}

int main(){
    return 0;
}