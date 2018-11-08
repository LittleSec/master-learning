/* 
 * 形态还原
 * 字典:dic_ec.txt
 */

#include<fstream>
#include<iostream>
#include<string>
#include<vector>
#include<map>
#include<algorithm>

using namespace std;

string split_char = " ";

void SplitString(const string& s, vector<string>& res, const string& c){
    string::size_type pos1, pos2;
    pos2 = s.find(c);
    pos1 = 0;
    while(pos2 != string::npos){
        res.push_back(s.substr(pos1, pos2-pos1));
        pos1 = pos2 + c.size();
        pos2 = s.find(c, pos1);
    }
    if(pos1 != s.length()){
        res.push_back(s.substr(pos1));
    }
}

class Dict{
    public:
        Dict();
        Dict(string& filename);
        bool isInDict(const string& s);
        void setDict(string& filename);
        void showDict(int num=10);
        bool showWord(const string& s, bool err_handler);
        ~Dict();
    private:
        long dict_size;
        map<string, vector<string> > dict;
        // vector<string> dict;
        string filename;
};

Dict::Dict(string& filename){
    this->filename = filename;
    setDict(filename);
}

bool Dict::isInDict(const string& s){
    if(dict.find(s) != dict.end()){
        return true;
    }
    else{
        return false;
    }
}

void Dict::setDict(string& filename){
    ifstream dict_file;
    dict_file.open(filename, ios::in);
    string s;
    string en;
    vector<string> explanation_vec;
    vector<string> part_of_speech_vec;
    while(getline(dict_file, s))
    {
        // cout << s << endl;
        explanation_vec.clear();
        part_of_speech_vec.clear();
        string::size_type en_expl_pos = s.find(split_char); // 必有一个split_char即默认不存在找不到的情况
        en = s.substr(0, en_expl_pos);
        SplitString(s.substr(en_expl_pos+1), explanation_vec, split_char);
        for(vector<string>::iterator it = explanation_vec.begin(); it != explanation_vec.end(); it++){
            if(it->find(".") == it->length()-1){ // 词性都是以.结尾
                part_of_speech_vec.push_back(*it);
            }
        }
        dict.insert(make_pair(en, part_of_speech_vec));
    }
    dict_file.close();
}

void Dict::showDict(int num){
    if(dict.empty()){
        cout << "dict is empty!" << endl;
    }
    else if(num > dict.size() || num <= 0){
        cout << "error param!" << endl;
    }
    else{
        int i;
        map<string, vector<string> >::iterator cn_iter = dict.begin();        
        for(i = 0; i < num; i++, cn_iter++){
            cout << cn_iter->first << " : ";
            vector<string>::iterator en_iter = cn_iter->second.begin();
            for(; en_iter != cn_iter->second.end()-1; en_iter++){
                cout << *en_iter << ",";
            }
            cout << *en_iter << endl;
        }
    }
}

bool Dict::showWord(const string& s, bool err_handler){
    if(err_handler && dict.empty()){
        cout << "Dict is empty!" << endl;
    }
    else if(err_handler && ! isInDict(s)){
        cout << "Not in Dict" << endl;
    }
    else if(isInDict(s)){
        cout << "Original from: " << s << endl;
        cout << "Part of speech: ";
        vector<string>::iterator it = dict[s].begin();
        for(; it != dict[s].end()-1; it++){
            cout << *it << ", ";
        }
        cout << *it << endl;
        return true;
    }
    return false;
}

Dict::~Dict(){
    dict.clear();
}

bool verbJudgeAndReduction(Dict& d, const string& word){
    string tmp;
    bool flag = d.showWord(word, false);
    if(!flag && word.substr(word.length()-1) == "s"){
        // *s -> * (SINGULAR3)
        tmp = word.substr(0, word.length()-1);
        flag = d.showWord(tmp, false);
    }
    if(!flag && word.substr(word.length()-2) == "es"){
        // *es -> * (SINGULAR3)
        tmp = word.substr(0, word.length()-2);
        flag = d.showWord(tmp, false);
    }
    if(!flag && word.substr(word.length()-3) == "ies"){
        // *ies -> *y (SINGULAR3)
        tmp = word.substr(0, word.length()-3) + "y";
        flag = d.showWord(tmp, false);
    }
    if(!flag && word.substr(word.length()-3) == "ing"){
        // *ing -> * (VING)
        tmp = word.substr(0, word.length()-3);
        flag = d.showWord(tmp, false);
    }
    if(!flag && word.substr(word.length()-3) == "ing"){
        // *ing -> *e (VING)
        tmp = word.substr(0, word.length()-3) + "e";
        flag = d.showWord(tmp, false);
    }
    if(!flag && word.substr(word.length()-4) == "ying"){
        // *ying -> *ie (VING)
        tmp = word.substr(0, word.length()-4) + "ie";
        flag = d.showWord(tmp, false);
    }
    if(!flag && word.substr(word.length()-3) == "ing"){
        // *??ing -> *? (VING)        
        tmp = word.substr(0, word.length()-4);
        flag = d.showWord(tmp, false);
    }
    if(!flag && word.substr(word.length()-2) == "ed"){
        // *ed -> * (PAST)(VEN)
        tmp = word.substr(0, word.length()-2);
        flag = d.showWord(tmp, false);
    }
    if(!flag && word.substr(word.length()-2) == "ed"){
        // *ed -> *e (PAST)(VEN)
        tmp = word.substr(0, word.length()-1);
        flag = d.showWord(tmp, false);
    }
    if(!flag && word.substr(word.length()-3) == "ied"){
        // *ied -> *y (PAST)(VEN)
        tmp = word.substr(0, word.length()-3) + "y";
        flag = d.showWord(tmp, false);
    }
    if(!flag && word.substr(word.length()-2) == "ed"){
        // *??ed -> *? (PAST)(VEN)
        tmp = word.substr(0, word.length()-3);
        flag = d.showWord(tmp, false);
    }
    return flag;
}

int main(int argc, char const *argv[])
{
    string filename = "dic_ec.txt"; 
    string verb;
    Dict d(filename);
    // d.showDict();
    // verbJudgeAndReduction(d, "finishied");
    while(cin >> verb){ // ctrl+d in unix-like system, ctrl+c in ms-dos
        if(!verbJudgeAndReduction(d, verb)){
            cout << "calling module of non-login dictionary... " << endl;
        };
    }
    return 0;
}
