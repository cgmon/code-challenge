from utils import parse_fasta, parse_fasta_yield, find_codons, find_codons_yield
import re, pytest, inspect


valid_data = """>NM_0002
augugcgag gacugcuga 
>NM_0003 
augugcgaguag""".splitlines()

valid_data_inline_comments = """augucgag >NM_0002
augugcgag""".splitlines()

invalid_data= """skip this""".splitlines()

invalid_data_char = """>NM_0002
auugcgad""".splitlines()

invalid_data_codon = """>NM_0002
auugccguaaa""".splitlines()

invalid_data_end = """>NM_0002
auugccgcc""".splitlines()



invalid_data_streams = """>NM_002
augugcgaguga
>NM_003
augugcd
""".splitlines()

########################################################
## Plain mode tests                                   ##
########################################################

def test_skips_non_relevant_initial_content():
    records = parse_fasta(invalid_data)
    assert len(records) == 0

def test_parses_all_applicable_sequences():
    records = parse_fasta(valid_data)
    assert len(records) == 2

def test_removes_whitespace_from_sequences():
    records = parse_fasta(valid_data)
    for record in records:
        assert not re.match(r'[\s]', record.sequence())

def test_raises_exception_invalid_char():
    with pytest.raises(Exception) as e_info:    
        records = parse_fasta(invalid_data_char)
        genes = find_codons(records)
    assert str(e_info.value)=='Invalid character found in sequence with id: NM_0002'

def test_raises_exception_invalid_codon():
    with pytest.raises(Exception) as e_info:
        records = parse_fasta(invalid_data_codon)
        genes = find_codons(records)
    assert str(e_info.value) == "Warning: Invalid codon AA found in sequence with id: NM_0002 and gene ['AUU', 'GCC', 'GUA']"

def test_raises_exception_invalid_end():
    with pytest.raises(Exception) as e_info:
        records = parse_fasta(invalid_data_end)
        genes = find_codons(records)
    assert str(e_info.value) == "Unexpected end of gene for sequence with id NM_0002 and gene ['AUU', 'GCC', 'GCC']"

def test_returns_genes_array():
    records = parse_fasta(valid_data)
    genes = find_codons(records)
    assert isinstance(genes, list)
    assert genes[0] == ['AUG','UGC','GAG','GAC','UGC','UGA']
    assert genes[1] == ['AUG','UGC','GAG','UAG']

def test_inline_comments():
    records = parse_fasta(valid_data_inline_comments)
    assert len(records) == 1


########################################################
## Streams mode tests                                 ##
########################################################

def test_streams_function_types():
    assert inspect.isgeneratorfunction(parse_fasta_yield)
    assert inspect.isgeneratorfunction(find_codons_yield)

def test_next_iterator():
    for record in parse_fasta_yield(valid_data):
        genes = find_codons_yield(record)
    next(genes)
    assert 1

def test_raises_exception_in_non_blocking_manner():
    genes = []
    for record in parse_fasta_yield(invalid_data_streams):
        for gene in find_codons_yield(record):
            genes.append(gene)
    assert len(genes) == 1