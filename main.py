import pandas as pd
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
import json

inputcsv = "input.csv"
outputcsv = "output.csv"
instelling = "dmg:" #"hva:", "industriemuseum:", "stam:", "archiefgent:"

#script om te controleren of objectnummers publieke manifesten hebben, en vraagt ook op hoeveel + welke beelden er publiek staan
#als input: een csv met alle objectnummers die webpublicatie Europeana hebben (of die publiek moeten staan op CoGent)

df_manifesten = pd.read_csv(inputcsv)
for i in range(len(df_manifesten)):
    try:
        response = urlopen("https://api.collectie.gent/iiif/presentation/v2/manifest/" + instelling + str(df_manifesten.loc[i, "objectnummer"]))
    except ValueError:
        df_manifesten.loc[i, "resultaten"] = "niet-publiek(value)"
    except HTTPError:
        df_manifesten.loc[i, "resultaten"] = "niet-publiek(http)"
    except URLError:
        df_manifesten.loc[i, "resultaten"] = "niet-publiek(url)"
    else:
        df_manifesten.loc[i, "resultaten"] = "publiek"
        data_json = json.loads(response.read())
        df_manifesten.loc[i, "aantalpubliekefotos"] = "/"
        for o in range(0, 100):
            try:
                afbeeldingurl = data_json["sequences"][0]['canvases'][o]["images"][0]["resource"]["@id"]
                print(afbeeldingurl)
            except IndexError:
                df_manifesten.loc[i, "aantalpubliekefotos"] = str(o) + " publiek(e) beeld(en)"
                break
            else:
                bestandsnaam = (afbeeldingurl.partition('-')[2]).partition('/')[0]
                bestandsnaam = bestandsnaam.replace("transcode-", "")
                df_manifesten.loc[i, "bestandsnaam"+str(o+1)] = bestandsnaam
    df_manifesten.to_csv(outputcsv)

#eventuele extra toevoegingen na lijn 35 'else'
#rechtentype > df_manifesten.loc[i, "rechtentype"+str(o+1)] = data_json["sequences"][0]['canvases'][0]["images"][0]["license"]
#attributies > df_manifesten.loc[i, "attributie"+str(o+1)] = data_json["sequences"][0]['canvases'][0]["images"][0]["attribution"]
#link webplatform >  df_manifesten.loc[i, "webplatform"] = "https://data.collectie.gent/entity/" + instelling + str(df_manifesten.loc[i, "objectnummer"]))