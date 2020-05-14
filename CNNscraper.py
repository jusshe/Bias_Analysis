import fileinput
from bs4 import BeautifulSoup
import urllib.request as client

# text to remove from articles
remove1 = "Donald TrumpSupreme CourtCongressFacts First2020 ElectionEditionU.S.InternationalArabicEspañolDonald TrumpSupreme CourtCongressFacts First2020 ElectionSearchEditionU.S.InternationalArabicEspañolUSCrime + JusticeEnergy + EnvironmentExtreme WeatherSpace + ScienceWorldAfricaAmericasAsiaAustraliaChinaEuropeIndiaMiddle EastUnited KingdomPoliticsDonald TrumpSupreme CourtCongressFacts First2020 ElectionBusinessMarketsTechMediaSuccessPerspectivesVideosOpinionPolitical Op-EdsSocial CommentaryHealthFoodFitnessWellnessParentingVital SignsEntertainmentStarsScreenBingeCultureMediaTechInnovateGadgetForeseeable FutureMission: AheadUpstartsWork TransformedInnovative CitiesStyleArtsDesignFashionArchitectureLuxuryBeautyVideoTravelDestinationsFood and DrinkStayNewsVideosSportsPro FootballCollege FootballBasketballBaseballSoccerOlympicsVideosLive TV Digital StudiosCNN FilmsHLNTV ScheduleTV Shows A-ZCNNVRCouponsCNN UnderscoredExploreWellnessGadgetsLifestyleCNN StoreMorePhotosLongformInvestigationsCNN ProfilesCNN LeadershipCNN NewslettersWork for CNNWeatherClimateStorm TrackerVideoFollow CNN Politics"
remove2 = "SearchUSCrime + JusticeEnergy + EnvironmentExtreme WeatherSpace + ScienceWorldAfricaAmericasAsiaAustraliaChinaEuropeIndiaMiddle EastUnited KingdomPoliticsDonald TrumpSupreme CourtCongressFacts First2020 ElectionBusinessMarketsTechMediaSuccessPerspectivesVideosOpinionPolitical Op-EdsSocial CommentaryHealthFoodFitnessWellnessParentingVital SignsEntertainmentStarsScreenBingeCultureMediaTechInnovateGadgetForeseeable FutureMission: AheadUpstartsWork TransformedInnovative CitiesStyleArtsDesignFashionArchitectureLuxuryBeautyVideoTravelDestinationsFood and DrinkStayNewsVideosSportsPro FootballCollege FootballBasketballBaseballSoccerOlympicsVideosLive TV Digital StudiosCNN FilmsHLNTV ScheduleTV Shows A-ZCNNVRCouponsCNN UnderscoredExploreWellnessGadgetsLifestyleCNN StoreMorePhotosLongformInvestigationsCNN ProfilesCNN LeadershipCNN NewslettersWork for CNNWeatherClimateStorm TrackerVideoFollow CNN PoliticsTerms of UsePrivacy PolicyAccessibility & CCAdChoicesAbout UsCNN Studio ToursCNN StoreNewslettersTranscriptsLicense FootageCNN NewsourceSitemap© 2020 Cable News Network.Turner Broadcasting System, Inc.All Rights Reserved.CNN Sans ™ & © 2016 Cable News Network."

baseUrl = "https://www.cnn.com/politics/article/sitemap-"  # ending is jan 2017: 2017-1.html

sitemapPages = []
for year in range(2017, 2020):
    sitemapPages += [baseUrl + str(year) + "-" + str(month) + ".html" for month in range(1, 13)]

sitemapPages += [baseUrl + "2020-1.html"]
sitemapPages += [baseUrl + "2020-2.html"]

# print urls
# for url in sitemapPages:
#    print(url + '\n')

allPoliticalArticles = []
for html_doc in sitemapPages:
    soup = BeautifulSoup(client.urlopen(html_doc), "html.parser")
    for link in soup.find_all('a'):
        allPoliticalArticles.append(link.get('href'))

allPoliticalArticles = [link for link in allPoliticalArticles if link.startswith("https://www.cnn.com/20") and "/politics/" in link]
for link in allPoliticalArticles:
    print(link)

for html_doc in fileinput.input():
    html_doc = html_doc.rstrip()
    article = BeautifulSoup(client.urlopen(html_doc), "html.parser")
    print(article.get_text().replace(remove1, "").replace(remove2, ""))


