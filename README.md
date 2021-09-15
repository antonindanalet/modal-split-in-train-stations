# Modal split of people going through a train station in Switzerland
This python script computes the modal split of trips going through Bern railway station. It selects the trips going through Bern railway station from the data of the <a href="https://www.are.admin.ch/mtmc">Mobility and Transport Microcensus (MTMC)</a> 2015, computes the main transport mode before and after going through the train station and saves the modal split before/after as CSV files <a href="https://github.com/antonindanalet/modal-split-in-train-stations/blob/master/data/output/modal_split_in_Bern_station_DE.csv">in German</a> and <a href="https://github.com/antonindanalet/modal-split-in-train-stations/blob/master/data/output/modal_split_in_Bern_station_FR.csv">in French</a>.

The results have been published as an infographic in the magazine of the <a href="https://www.are.admin.ch/">Swiss Federal Office for Spatial Development (ARE)</a> "<a href="https://www.are.admin.ch/are/de/home/medien-und-publikationen/forum-raumentwicklung.html">Forum Raumentwicklung</a>"/"<a href="https://www.are.admin.ch/are/fr/home/media-et-publications/forum-du-developpement-territorial.html">Forum du développement territorial</a>"/"<a href="https://www.are.admin.ch/are/it/home/media-e-pubblicazioni/forum-sviluppo-territoriale.html">Forum sviluppo territoriale</a>" in its <a href="https://www.are.admin.ch/are/de/home/medien-und-publikationen/forum-raumentwicklung/vernetzte-mobilitat.html">edition about combined mobility on page 9 in German</a> and <a href="https://www.are.admin.ch/are/fr/home/media-et-publications/forum-du-developpement-territorial/mobilitecombinee.html">on page 43 in French</a>. It has also been published on Twitter in <a href="https://twitter.com/nicole_mathys/status/1305832391534141440">German</a> and <a href="https://twitter.com/AntoninDanalet/status/1306222523667841024">in French</a>.

According to our definition of Bern railway station, 1444 trips are going through the railway station. These trips have been made by 706 single persons.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for reproducing the result and understanding how it has been generated.

### Prerequisites

To run the code itself, you need python 3 and pandas.

For it to produce the results, you also need the raw data of the Transport and Mobility Microcensus 2015, not included on GitHub. These data are individual data and therefore not open. You can however get them by filling in this form in <a href="https://www.are.admin.ch/are/de/home/verkehr-und-infrastruktur/grundlagen-und-daten/mzmv/datenzugang.html">German</a>, <a href="https://www.are.admin.ch/are/fr/home/mobilite/bases-et-donnees/mrmt/accesauxdonnees.html">French</a> or <a href="https://www.are.admin.ch/are/it/home/mobilita/basi-e-dati/mcmt/accessoaidati.html">Italian</a>. The cost of the data is available in the document "<a href="https://www.are.admin.ch/are/de/home/medien-und-publikationen/publikationen/grundlagen/mikrozensus-mobilitat-und-verkehr-2015-mogliche-zusatzauswertung.html">Mikrozensus Mobilität und Verkehr 2015: Mögliche Zusatzauswertungen</a>"/"<a href="https://www.are.admin.ch/are/fr/home/media-et-publications/publications/bases/mikrozensus-mobilitat-und-verkehr-2015-mogliche-zusatzauswertung.html">Microrecensement mobilité et transports 2015: Analyses supplémentaires possibles</a>".

### Run the code

Please copy the file <em>etappen.csv</em> that you receive from the Federal Statistical Office in the folder "<a href="https://github.com/antonindanalet/modal-split-in-train-stations/tree/master/data/input">data/input</a>". Then run <em><a href="https://github.com/antonindanalet/modal-split-in-train-stations/blob/master/src/run_modal_split_in_train_stations.py">src/run_modal_split_in_train_stations.py</a></em>. 

DO NOT commit or share in any way the CSV-files <em>etappen.csv</em>! These are personal data.

## Contact

Please don't hesitate to contact me if you have questions or comments about this code: antonin.danalet@are.admin.ch
