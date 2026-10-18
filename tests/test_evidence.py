import pytest
from focuslab_core.evidence import retrieve_evidence, validate_evidence_ids, tokenize

def sample():
    return [{'id':'A','title':'Task switching','sourceUrl':'https://example.com/a','summary':'Switching tasks costs time','passages':['task switch cost'],'limitations':'small sample'}, {'id':'B','title':'Rest breaks','sourceUrl':'https://example.com/b','summary':'Breaks can help recovery','passages':['break and recovery'],'limitations':'varies'}]

def test_retrieval_ranks_relevant():
    out=retrieve_evidence('task switching',k=2,entries=sample())
    assert out and out[0]['id']=='A'

def test_invalid_evidence_reference():
    with pytest.raises(ValueError): validate_evidence_ids(['NOPE'],sample())
    assert validate_evidence_ids(['A','A'],sample())==['A']

def test_tokenize(): assert tokenize('Hello, FocusLab 42')==['hello','focuslab','42']
