class Word(object):
    # 这个事实上就是 coNLL 标准的依存句法格式啦
    def __init__(self, string):
        self.index, self.form, self.lemma, self.cpostag, self.postag, self.feats, self.head, self.deprel = string.strip().split()
        self.index = int(self.index)
        self.head = int(self.head)
        self.child_list = list()
        
    def set_head(self, head):
        self.head = head
    
    def set_form(self, form):
        self.form = form
    
    def set_index(self, index):
        self.index = index
    
    def set_cpostag(self, cpostag):
        self.cpostag = cpostag
    
    def set_postag(self, postag):
        self.postag = postag
        
    def get_child(self, idx):
        return self.child_list[idx].index

class ParseStack(list):
    # 写一个基于list的派生类，而不是一个内部封装了一个list的类，这样子或许简洁一些
    def empty(self):
        return len(self) == 0 

    def push(self, item):
        self.append(item)

    def top(self, idx=1):
        if len(self) >= idx:
            return self[-1 * idx]

    def size(self):
        return len(self) 

    def left_arc(self):
        top1 = self.pop()
        top2 = self.pop()
        top1.child_list.append(top2)
        self.push(top1)
    
    def right_arc(self):
        top1 = self.pop()
        top2 = self.pop()
        top2.child_list.append(top1)
        self.push(top2)

    def shift(self, queue):
        self.push(queue.get())
    
class ParseQueue(list):
    # 写一个基于list的parse队列
    def put(self, item):
        self.append(item)

    def get(self):
        return self.pop(0)
    
    def queue_head(self, idx=1):
        if len(self) >= idx:
            return self[idx -1]

    def empty(self):
        return len(self) == 0

    def all_heads(self):
        return set([item.head for item in self])

def read_a_sentence(file):
    # file是一个文件对象,函数返回一个list of Words
    while True:
        buff = []
        line = file.readline()
        while line and line.strip():
            buff.append(Word(line))
            line = file.readline()
        yield buff
    
def generate(sentence):
    parse_stack = ParseStack()
    ROOT = Word("0\tROOT\tROOT\tROOT\tROOT\t_\t0\tROOT")
    parse_stack.push(ROOT)
    parse_queue = ParseQueue(sentence)
    print(len(sentence), end=' ')
    print(''.join([w.form for w in sentence]))
    
    while True:
        if parse_stack.size() >= 2:
            #print("栈元素大于等于2")
            if parse_stack.top(2).head == parse_stack.top().index and parse_stack.top(2).index not in parse_queue.all_heads():
                print("{} <-- {}".format(parse_stack.top(2).form, parse_stack.top().form))
                # yield "left_arc"
                parse_stack.left_arc()
            elif parse_stack.top().head == parse_stack.top(2).index and parse_stack.top().index not in parse_queue.all_heads():
                print("{} --> {}".format(parse_stack.top(2).form, parse_stack.top().form))
                # yield "right_arc"
                parse_stack.right_arc()
            elif not parse_queue.empty():
                print("不能左规约或者右规约, 且队列未空, 故移进: {}".format(parse_queue.queue_head().form))
                parse_stack.shift(parse_queue)
                # yield "shift"
            else:
                print("句子不合法\n")
                break
        elif not parse_stack.top().child_list:
            print("初始的移进: {}".format(parse_queue.queue_head().form))
            parse_stack.shift(parse_queue)
        elif parse_queue.empty():
            print("已经规约成为句子了\n")
            break
        else:
            print("句子不合法\n")
            break



if __name__ == "__main__":
    f = open("./HIT_train.conll", 'rt')
    sents = read_a_sentence(f)
    for sent in sents:
        generate(sent)
