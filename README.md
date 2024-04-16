# Plat Analysis

## Summary

Initially conceived as a straightforward processor for homeowners association restriction documents, this project aimed to extract and store pertinent information. However, it has since evolved to accommodate a diverse range of document types and supports storage across multiple database systems.

In recent months, the project has further expanded due to an influx of historical newspaper clippings and other document images. This has necessitated the incorporation of more sophisticated image extraction techniques. Additionally, the project now includes the development of a text classifier, sentiment analysis, and various other text analysis tools.




## TODO

1. - [ ] Find a way to avoid installing java by getting rid of tika.
1. - [ ] Add textract for additional metadata information.
1. - [ ] For searchable pdfs, extract the text and store it in the database.
1. - [ ] Document should take all potential file types and match rather than testing internally.
1. - [ ] In the pdfprocessor object, collect metadata about the file and merge it into the writer object.
1. - [ ] [Text analysis with mongodb](https://mikeharmonphd.medium.com/sentiment-analysis-part-2-4338c02315c3)
1. - [ ] Add sqlwriter
1. - [ ] Deal with these file names
1. - [ ] Add filetypes
1. - [ ] Come back to struct errors and figure out what is going on
1. - [ ] Can I remove watermarks?
1. - [ ] Convert the file write to use a protocol and implement a sqlwriter
1. - [ ] Resolve `WARNING:plat.ocr:Not implemented error on pages in pdf plat/data/GRAND MESA/Grand Mesa 7 Lots 83 and 84 Replat Addressing 2019-07-30 (2).pdf: unsupported filter /JBIG2Decode. File path: plat/data/GRAND MESA/Grand Mesa 7 Lots 83 and 84 Replat Addressing 2019-07-30 (2).pdf`
1. - [ ] Collect additional pdf file properties.
1. - [ ] Secure u/p
1. - [ ] Rename plat to src
1. - [ ] Remove watermarks
1. - [ ] Image analysis
1. - [ ] Opencv
1. - [ ] OCR document
1. - [ ] Store text data
1. - [ ] Analyse text data
1. - [ ] Store image data in mongodb

## Mongo Details

```shell
"IPAddress": "172.19.0.3",
"DNSNames": [
    "plat_analysis_devcontainer-mongo-1",
    "mongo",
    "18470a4f9382"
]
```


## Setup

```shell
make build
```
