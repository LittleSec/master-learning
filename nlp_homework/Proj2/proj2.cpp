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
        bool isInDict(string& s);
        void setDict(string& filename);
        void showDict(int num=10);
        ~Dict();
        // should be private
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
    dict_file.imbue(locale("zh_CN.UTF-8"));
    string s;
    string cn;
    vector<string> en_vector;
    while(getline(dict_file, s))
    {
        // cout << s << endl;
        en_vector.clear();
        string::size_type cn_en_pos = s.find(split_char); // 必有一个split_char即默认不存在找不到的情况
        cn = s.substr(0, cn_en_pos);
        SplitString(s.substr(cn_en_pos+1), en_vector, split_char);
        dict.insert(make_pair(cn, en_vector));
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

Dict::~Dict(){
    dict.clear();
}

void FMM(string& seq, Dict& d, vector<string>& splic_word_res){
    // string::size_type是无符号，意味着：如果是<0作为条件的话，是永真的！
    int i = 0;
    string tmp;
    while(i < seq.length()){ 
        // 不能j = seq.length()/3，因为substr()不通用！
        for(int j = seq.length(); j > i; j-=3){
            tmp = seq.substr(i, j-i); // substr(start, length)
            // cout << i << " " <<  j << " " << tmp << endl;  
            if(tmp.length() == 3){
                splic_word_res.push_back(tmp);
            }
            else if(d.isInDict(tmp)){
                splic_word_res.push_back(tmp);
                i = i + (tmp.length() - 3);
            }
        }
        i+=3;
    }
}

void RMM(string& seq, Dict& d, vector<string>& splic_word_res){
    int i = seq.length();
    string tmp;
    while(i > 0){
        for(int j = 0; j < seq.length(); j+=3){
            if(i <= j){
                break;
            }
            tmp = seq.substr(j, i-j);
            if(tmp.length() == 3){
                splic_word_res.push_back(tmp);
            }
            else if(d.isInDict(tmp)){
                splic_word_res.push_back(tmp);
                i = i - (tmp.length()-3);
            }
        }
        i-=3;
    }
    reverse(splic_word_res.begin(), splic_word_res.end());
}

int main(int argc, char const *argv[]){
    string sequence = "细胞分裂组织";
    string filename = "ce.txt";
    Dict d(filename);
    vector<string> fm;
    vector<string> rm;
    // cin >> sequence;
    // cout << d.dict.size() << endl;
    // d.showDict(10);
    FMM(sequence, d, fm);
    for(vector<string>::iterator it = fm.begin(); it != fm.end(); it++){
        cout << *it << '/';
    }
    cout << endl;

    RMM(sequence, d, rm);
    for(vector<string>::iterator it = rm.begin(); it != rm.end(); it++){
        cout << *it << '/';
    }
    cout << endl;

    return 0;
}