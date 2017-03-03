# SoundBrowser

This repository provides an interface for the VU Sound Corpus, made in Flask.
Use `python soundbrowser.py` to run it locally on `http://127.0.0.1:5000/`.
If you use this work, please cite [this paper](http://www.lrec-conf.org/proceedings/lrec2016/summaries/206.html):
```
@InProceedings{VANMILTENBURG16.206,
  author = {Emiel van Miltenburg and Benjamin Timmermans and Lora Aroyo},
  title = {The VU Sound Corpus: Adding More Fine-grained Annotations to the Freesound Database},
  booktitle = {Proceedings of the Tenth International Conference on Language Resources and Evaluation (LREC 2016)},
  year = {2016},
  month = {may},
  date = {23-28},
  location = {Portorož, Slovenia},
  editor = {Nicoletta Calzolari (Conference Chair) and Khalid Choukri and Thierry Declerck and Sara Goggi and Marko Grobelnik and Bente Maegaard and Joseph Mariani and Helene Mazo and Asuncion Moreno and Jan Odijk and Stelios Piperidis},
  publisher = {European Language Resources Association (ELRA)},
  address = {Paris, France},
  isbn = {978-2-9517408-9-1},
  language = {english}
 } 
```

**Requirements**

* Flask
* lxml
* Tested with Python 3.4, but other versions probably work just fine.

## Screenshot
Here's an image of the basic interface. The special keyword 'all' gives you all the sounds from the corpus. Other queries work as you would expect.

<img src="images/screenshot.png" width="400px">

## More information
More information about the corpus can be found [here](https://github.com/CrowdTruth/vu-sound-corpus).
