from Sequence import Sequence
import re

stop_codons = ['UAG', 'UGA', 'UAA']

def parse_fasta(source):
    id, seq = None, []
    genes = []
    for line in source:
        line = line.rstrip()
        comment_position = re.search(">", line)
        if comment_position:
            if id: genes.append(Sequence(id=id, seq="".join(seq).replace(" ","").replace("\r", "").upper()))
            id, seq = line[comment_position.end():], [] 
        else:
            seq.append(line)
    if id: genes.append(Sequence(id=id, seq="".join(seq).replace(" ","").replace("\r", "").upper()))

    return genes
def parse_fasta_yield(source):
    id, seq = None, []
    for line in source:
        line = line.rstrip()
        comment_position = re.search(">", line)
        if comment_position:
            if id: yield Sequence(id=id, seq="".join(seq).replace(" ","").replace("\r", "").upper())
            id, seq = line[comment_position.end():], []     
        else:
            seq.append(line)  
    if id: yield Sequence(id=id, seq="".join(seq).replace(" ","").replace("\r", "").upper())  

def find_codons(records):
    genes = []
    for record in records:
        seq = record.sequence()
        assert re.match('[AUGC]+$', seq), f"Invalid character found in sequence with id: {record.id}"
        n = len(seq)
        codons = []
        for i in range(0, n, 3):
            codon = seq[i:i+3]
            assert len(codon) == 3, f"Warning: Invalid codon {codon} found in sequence with id: {record.id} and gene {codons}"
            codons.append(codon)
            if(codon in stop_codons and len(codons) >=3):
                genes.append(codons)
                codons = []
        if(len(codons)):
            raise Exception(f'Unexpected end of gene for sequence with id {record.id} and gene {codons}')
    return genes

def find_codons_yield(record):
    codons = []
    has_yielded=False
    try:
        seq = record.sequence()
        assert re.match('[AUGC]+$', seq), f"Invalid character found in sequence with id: {record.id}"
        n = len(seq)
        for i in range(0, n, 3):
            codon = seq[i:i+3]
            assert len(codon) == 3, f"Warning: Invalid codon {codon} found in sequence with id: {record.id} and gene {codons}"
            codons.append(codon)
            if(codon in stop_codons and len(codons) >= 3):
                yield(codons)
                has_yielded=True
                codons = []
    except AssertionError as e:
        if(not has_yielded): 
            print(f'Warning: Unexpected end of gene for sequence with id {record.id} and gene {codons}')
        else: 
            print(e)

def lazy_iterator():
    with open(input("Local filename path:"), 'r') as data:
        for record in parse_fasta_yield(data):
            for gene in find_codons_yield(record):
                print(gene)   

def iterator():
    genes = []
    with open(input("Local filename path:"), 'r') as data:
        records = parse_fasta(data)
        genes = find_codons(records)
        print(genes)


            