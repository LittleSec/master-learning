/* 
 * 中文分词系统
 * 字典:ce.txt
*/

#include<fstream>
#include<iostream>
#include<string>
#include<vector>
#include<map>
#include<algorithm>

using namespace std;

string split_char = ",";
/* 
 * params:
 * s: source string
 * res: split substrings
 * c: split char(usually ',')
 * ref:https://www.cnblogs.com/lyf-sunicey/p/8489472.html
 */
void SplitString(const string& s, vector<string>& res, const string& c)
{
    string::size_type pos1, pos2;
    pos2 = s.find(c);
    pos1 = 0;
    while(pos2 != string::npos)
    {
        res.push_back(s.substr(pos1, pos2-pos1));
        pos1 = pos2 + c.size();
        pos2 = s.find(c, pos1);
    }
    if(pos1 != s.length())
        res.push_back(s.substr(pos1));
}

class Dict{
    public:
        Dict();
        Dict(string& filename);
        bool isInDict(string& s);
        void setDict(string& filename);
        map<string, vector<string> > dict;
        ~Dict();
    private:
        long dict_size;
        // vector<string> dict;
        string filename;
};

Dict::Dict(string& filename){
    this->filename = filename;
    setDict(filename);
}

bool Dict::isInDict(string& s){
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
    string cn;
    vector<string> en;
    while(getline(dict_file, s))
    {
        // cout << s << endl;
        en.clear();
        string::size_type cn_en_pos = s.find(split_char);
        cn = s.substr(0, cn_en_pos);
        SplitString(s.substr(cn_en_pos), en, split_char);
        dict.insert(make_pair(cn, en));
    }
    dict_file.close();
}

Dict::~Dict(){
    dict.clear();
}

void RMM(string seq, Dict d, vector<string>& splic_word_res){
    string::size_type i = seq.size();
    while(i > 0){
        for(string::size_type j = 0; j < seq.size(); j++){
            string tmp = seq.substr(j, i);
            if(tmp.size() == 1){
                splic_word_res.push_back(tmp);
            }
            else if(d.isInDict(tmp)){
                splic_word_res.push_back(tmp);
                i = i - (tmp.size()-1);
            }
        }
        i--;
    }
    reverse(splic_word_res.begin(), splic_word_res.end());
}

void FMM(string seq, Dict d, vector<string>& splic_word_res){
    string::size_type i = 0;
    while(i < seq.size()){
        for(string::size_type j = seq.size(); j >= 0; j--){
            string tmp = seq.substr(i, j);
            if(tmp.size() == 1){
                splic_word_res.push_back(tmp);
            }
            else if(d.isInDict(tmp)){
                splic_word_res.push_back(tmp);
                i = i + (tmp.size() - 1);
            }
        }
        i++;
    }
}

int main(){
    string sequence;
    string filename = "ce.txt";
    Dict d(filename);
    vector<string> fm;
    vector<string> rm;
    cin >> sequence;
    // for(map<string, vector<string> >::iterator iter = d.dict.begin(); iter != d.dict.end(); iter++){
    //     cout << iter->first << endl;
    // } 
    cout << d.dict.size() << endl;
    /*
    RMM(sequence, d, rm);
    FMM(sequence, d, fm);
    for(vector<string>::iterator it = fm.begin(); it != fm.end(); it++){
        cout << *it << '/';
    }
    cout << endl;
    for(vector<string>::iterator it = rm.begin(); it != fm.end(); it++){
        cout << *it << '/';
    }
    cout << endl;
    */
    return 0;
}