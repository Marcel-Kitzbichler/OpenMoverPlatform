from pathlib import Path

def parse(kmlfilePath):
    kmlfile = Path(kmlfilePath).read_text().replace('\n', '')
    #delete every space and tab in the kml file
    kmlfile = kmlfile.replace(' ', '').replace('\t', '')
    kmlfile = kmlfile.split('<LineString><coordinates>')[1]
    kmlfile = kmlfile.split('</coordinates></LineString>')[0]
    kmlfile = kmlfile.split(',')[:-1]
    for i in range(len(kmlfile)):
        kmlfile[i] = int(float(kmlfile[i])*100000000000000)
    return kmlfile