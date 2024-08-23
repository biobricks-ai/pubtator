# PubTator3

## Description

PubTator3 (https://www.ncbi.nlm.nih.gov/research/pubtator3/) is a web service for exploring and retrieving bioconcept and relation annotations in biomedical articles. PubTator3 provides automated annotations from state-of-the-art deep learning-based text mining systems for genes/proteins, genetic variants, diseases, chemicals, species, cell lines and the relations among the entities, all available for immediate download. PubTator3 annotates PubMed (36 million abstracts), the PMC Open Access Subset and the Author Manuscript Collection (6.3 million full text articles).  This FTP repository aggregated all the bio-entity and relation annotations in PubTator3 in BioC-XML and PubTator (tab-separated) formats. The files are expected to be updated monthly.

## Contents

### BioC
    Has the archivements of the abstracts and full texts with entity/relation annotations of the entire PubTator3.
    
    Rows: 

    Columns:
    - **ID**: The unique identifier of the document.
    - **Title**: The title of the document.
    - **Abstract**: The abstract of the document.
    - **Authors**
    - **Annotations**

### gene2pubtator3

    Results are from AIONER for NER and GNormPlus for normalization.

### disease2pubtator3

    Results are from AIONER for NER and TaggerOne for normalization.

### chemical2pubtator3

    Results are from AIONER for NER and NLM-Chem for normalization.

### species2pubtator3

    Results are from AIONER for NER and GNorm2 for normalization.

### mutation2pubtator3

    Results are from tmVar3.

### cellline2pubtator3

    Results are from AIONER for NER and TaggerOne for normalization.

### bioconcepts2pubtator3

    Combination of all entity annotations in PubTator3.

### relation2pubtator3

    Whole set of relations extracted by BioREx.

	