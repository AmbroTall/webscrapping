import pandas as pd
from match import Match
from thefuzz import process
from db import *
import time
import network_utils as nu

headers = {
  'authority': 'als.dafabet.com',
  'accept': 'application/json',
  'Accept-Encoding': 'gzip',
  'accept-language': 'en-GB',
  'referer': 'https://www.dafabet.com/en/sports-df/sports',
  'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
}
def dafabetALP():
    url = "https://als.dafabet.com/xapi/rest/events?bettable=true&marketStatus=OPEN&periodType=PRE_MATCH&includeMarkets=true&includeHiddenOutcomes=true&includeHiddenMarkets=false&maxMarketPerEvent=100&lightWeightResponse=true&sportGroups=REGULAR&allBettableEvents=true&marketFilter=GAME&eventType=GAME&excludeMarketByOpponent=true&marketTypeIds=12%2C3021%2C13%2C3007%2C1%2C29%2C2101%2C2722&periodIds=100%2C102%2C232%2C233%2C234%2C11511&includeAdditional=false&additionalMarketTypeIds=479%2C110124%2C13004%2C13005%2C13000&additionalPeriodIds=100%2C102%2C232%2C234&sortMarketsByPriceDifference=true&includeLiveEvents=true&sportCodes=FOOT%2CTENN%2CBASK%2CBASE%2CVOLL%2CBADM%2CICEH%2CAMFB%2CRUGL%2CRUGU%2CTABL%2CSNOO%2CDART%2CCRIC%2CHAND%2CEFOT%2CEBSK%2CVICR%2CFUTS%2CBEVO&liveMarketStatus=OPEN%2CSUSPENDED&liveAboutToStart=true&liveExcludeLongTermSuspended=true&eventPathIds=23489&maxMarketsPerMarketType=1&sortByEventpath=true&sortByEventpathIds=240%2C227%2C24158235%2C22895%2C23091%2C22942%2C102490%2C22962%2C22920%2C35454808%2C32415090%2C31938288%2C25914812%2C239%2C226%2C215%2C99917500%2C10199131%2C10399131%2C2500%2C249%2C250%2C1%2C3700%2C5000%2C1700%2C1250%2C3400%2C238%2C2700%2C22886%2C22889%2C3500%2C1600%2C237%2C1100%2C2100%2C22881%2C1300%2C50%2C22888%2C22878%2C22877%2C22884%2C3%2C1900%2C10399132%2C1200%2C1400%2C2900%2C2%2C10999130%2C1800%2C5%2C3300%2C10999126%2C10999125%2C10999127%2C4%2C10999123%2C6%2C10999124%2C10999129%2C10999128&page=1&eventsPerPage=70&l=en"
    return dafabetGetData(url, "ALP")
def dafabetBSA():
    url = "https://als.dafabet.com/xapi/rest/events?bettable=true&marketStatus=OPEN&periodType=PRE_MATCH&includeMarkets=true&includeHiddenOutcomes=true&includeHiddenMarkets=false&maxMarketPerEvent=100&lightWeightResponse=true&sportGroups=REGULAR&allBettableEvents=true&marketFilter=GAME&eventType=GAME&excludeMarketByOpponent=true&marketTypeIds=12%2C3021%2C13%2C3007%2C1%2C29%2C2101%2C2722&periodIds=100%2C102%2C232%2C233%2C234%2C11511&includeAdditional=false&additionalMarketTypeIds=479%2C110124%2C13004%2C13005%2C13000&additionalPeriodIds=100%2C102%2C232%2C234&sortMarketsByPriceDifference=true&includeLiveEvents=true&sportCodes=FOOT%2CTENN%2CBASK%2CBASE%2CVOLL%2CBADM%2CICEH%2CAMFB%2CRUGL%2CRUGU%2CTABL%2CSNOO%2CDART%2CCRIC%2CHAND%2CEFOT%2CEBSK%2CVICR%2CFUTS%2CBEVO&liveMarketStatus=OPEN%2CSUSPENDED&liveAboutToStart=true&liveExcludeLongTermSuspended=true&eventPathIds=22980&maxMarketsPerMarketType=1&sortByEventpath=true&sortByEventpathIds=240%2C227%2C24158235%2C22895%2C23091%2C22942%2C102490%2C22962%2C22920%2C35454808%2C32415090%2C31938288%2C25914812%2C239%2C226%2C215%2C99917500%2C10199131%2C10399131%2C2500%2C249%2C250%2C1%2C3700%2C5000%2C1700%2C1250%2C3400%2C238%2C2700%2C22886%2C22889%2C3500%2C1600%2C237%2C1100%2C2100%2C22881%2C1300%2C50%2C22888%2C22878%2C22877%2C22884%2C3%2C1900%2C10399132%2C1200%2C1400%2C2900%2C2%2C10999130%2C1800%2C5%2C3300%2C10999126%2C10999125%2C10999127%2C4%2C10999123%2C6%2C10999124%2C10999129%2C10999128&page=1&eventsPerPage=70&l=en"
    return dafabetGetData(url, "BSA")
def dafabetBSB():
    url = "https://als.dafabet.com/xapi/rest/events?bettable=true&marketStatus=OPEN&periodType=PRE_MATCH&includeMarkets=true&includeHiddenOutcomes=true&includeHiddenMarkets=false&maxMarketPerEvent=100&lightWeightResponse=true&sportGroups=REGULAR&allBettableEvents=true&marketFilter=GAME&eventType=GAME&excludeMarketByOpponent=true&marketTypeIds=12%2C3021%2C13%2C3007%2C1%2C29%2C2101%2C2722&periodIds=100%2C102%2C232%2C233%2C234%2C11511&includeAdditional=false&additionalMarketTypeIds=479%2C110124%2C13004%2C13005%2C13000&additionalPeriodIds=100%2C102%2C232%2C234&sortMarketsByPriceDifference=true&includeLiveEvents=true&sportCodes=FOOT%2CTENN%2CBASK%2CBASE%2CVOLL%2CBADM%2CICEH%2CAMFB%2CRUGL%2CRUGU%2CTABL%2CSNOO%2CDART%2CCRIC%2CHAND%2CEFOT%2CEBSK%2CVICR%2CFUTS%2CBEVO&liveMarketStatus=OPEN%2CSUSPENDED&liveAboutToStart=true&liveExcludeLongTermSuspended=true&eventPathIds=24267&maxMarketsPerMarketType=1&sortByEventpath=true&sortByEventpathIds=240%2C227%2C24158235%2C22895%2C23091%2C22942%2C102490%2C22962%2C22920%2C35454808%2C32415090%2C31938288%2C25914812%2C239%2C226%2C215%2C99917500%2C10199131%2C10399131%2C2500%2C249%2C250%2C1%2C3700%2C5000%2C1700%2C1250%2C3400%2C238%2C2700%2C22886%2C22889%2C3500%2C1600%2C237%2C1100%2C2100%2C22881%2C1300%2C50%2C22888%2C22878%2C22877%2C22884%2C3%2C1900%2C10399132%2C1200%2C1400%2C2900%2C2%2C10999130%2C1800%2C5%2C3300%2C10999126%2C10999125%2C10999127%2C4%2C10999123%2C6%2C10999124%2C10999129%2C10999128&page=1&eventsPerPage=70&l=en"
    return dafabetGetData(url, "BSB")
def dafabetCPA():
    url = "https://als.dafabet.com/xapi/rest/events?bettable=true&marketStatus=OPEN&periodType=PRE_MATCH&includeMarkets=true&includeHiddenOutcomes=true&includeHiddenMarkets=false&maxMarketPerEvent=100&lightWeightResponse=true&sportGroups=REGULAR&allBettableEvents=true&marketFilter=GAME&eventType=GAME&excludeMarketByOpponent=true&marketTypeIds=12%2C3021%2C13%2C3007%2C1%2C29%2C2101%2C2722&periodIds=100%2C102%2C232%2C233%2C234%2C11511&includeAdditional=false&additionalMarketTypeIds=479%2C110124%2C13004%2C13005%2C13000&additionalPeriodIds=100%2C102%2C232%2C234&sortMarketsByPriceDifference=true&includeLiveEvents=true&sportCodes=FOOT%2CTENN%2CBASK%2CBASE%2CVOLL%2CBADM%2CICEH%2CAMFB%2CRUGL%2CRUGU%2CTABL%2CSNOO%2CDART%2CCRIC%2CHAND%2CEFOT%2CEBSK%2CVICR%2CFUTS%2CBEVO&liveMarketStatus=OPEN%2CSUSPENDED&liveAboutToStart=true&liveExcludeLongTermSuspended=true&eventPathIds=18205655&maxMarketsPerMarketType=1&sortByEventpath=true&sortByEventpathIds=240%2C227%2C24158235%2C22895%2C23091%2C22942%2C102490%2C22962%2C22920%2C35454808%2C32415090%2C31938288%2C25914812%2C239%2C226%2C215%2C99917500%2C10199131%2C10399131%2C2500%2C249%2C250%2C1%2C3700%2C5000%2C1700%2C1250%2C3400%2C238%2C2700%2C22886%2C22889%2C3500%2C1600%2C237%2C1100%2C2100%2C22881%2C1300%2C50%2C22888%2C22878%2C22877%2C22884%2C3%2C1900%2C10399132%2C1200%2C1400%2C2900%2C2%2C10999130%2C1800%2C5%2C3300%2C10999126%2C10999125%2C10999127%2C4%2C10999123%2C6%2C10999124%2C10999129%2C10999128&page=1&eventsPerPage=70&l=en"
    return dafabetGetData(url, "CPA")
def dafabetCPB():
    url = "https://als.dafabet.com/xapi/rest/events?bettable=true&marketStatus=OPEN&periodType=PRE_MATCH&includeMarkets=true&includeHiddenOutcomes=true&includeHiddenMarkets=false&maxMarketPerEvent=100&lightWeightResponse=true&sportGroups=REGULAR&allBettableEvents=true&marketFilter=GAME&eventType=GAME&excludeMarketByOpponent=true&marketTypeIds=12%2C3021%2C13%2C3007%2C1%2C29%2C2101%2C2722&periodIds=100%2C102%2C232%2C233%2C234%2C11511&includeAdditional=false&additionalMarketTypeIds=479%2C110124%2C13004%2C13005%2C13000&additionalPeriodIds=100%2C102%2C232%2C234&sortMarketsByPriceDifference=true&includeLiveEvents=true&sportCodes=FOOT%2CTENN%2CBASK%2CBASE%2CVOLL%2CBADM%2CICEH%2CAMFB%2CRUGL%2CRUGU%2CTABL%2CSNOO%2CDART%2CCRIC%2CHAND%2CEFOT%2CEBSK%2CVICR%2CFUTS%2CBEVO&liveMarketStatus=OPEN%2CSUSPENDED&liveAboutToStart=true&liveExcludeLongTermSuspended=true&eventPathIds=18205656&maxMarketsPerMarketType=1&sortByEventpath=true&sortByEventpathIds=240%2C227%2C24158235%2C22895%2C23091%2C22942%2C102490%2C22962%2C22920%2C35454808%2C32415090%2C31938288%2C25914812%2C239%2C226%2C215%2C99917500%2C10199131%2C10399131%2C2500%2C249%2C250%2C1%2C3700%2C5000%2C1700%2C1250%2C3400%2C238%2C2700%2C22886%2C22889%2C3500%2C1600%2C237%2C1100%2C2100%2C22881%2C1300%2C50%2C22888%2C22878%2C22877%2C22884%2C3%2C1900%2C10399132%2C1200%2C1400%2C2900%2C2%2C10999130%2C1800%2C5%2C3300%2C10999126%2C10999125%2C10999127%2C4%2C10999123%2C6%2C10999124%2C10999129%2C10999128&page=1&eventsPerPage=70&l=en"
    return dafabetGetData(url, "CPB")
def dafabetELP():
    url = "https://als.dafabet.com/xapi/rest/events?bettable=true&marketStatus=OPEN&periodType=PRE_MATCH&includeMarkets=true&includeHiddenOutcomes=true&includeHiddenMarkets=false&maxMarketPerEvent=100&lightWeightResponse=true&sportGroups=REGULAR&allBettableEvents=true&marketFilter=GAME&eventType=GAME&excludeMarketByOpponent=true&marketTypeIds=12%2C3021%2C13%2C3007%2C1%2C29%2C2101%2C2722&periodIds=100%2C102%2C232%2C233%2C234%2C11511&includeAdditional=false&additionalMarketTypeIds=479%2C110124%2C13004%2C13005%2C13000&additionalPeriodIds=100%2C102%2C232%2C234&sortMarketsByPriceDifference=true&includeLiveEvents=true&sportCodes=FOOT%2CTENN%2CBASK%2CBASE%2CVOLL%2CBADM%2CICEH%2CAMFB%2CRUGL%2CRUGU%2CTABL%2CSNOO%2CDART%2CCRIC%2CHAND%2CEFOT%2CEBSK%2CVICR%2CFUTS%2CBEVO&liveMarketStatus=OPEN%2CSUSPENDED&liveAboutToStart=true&liveExcludeLongTermSuspended=true&eventPathIds=168610&maxMarketsPerMarketType=1&sortByEventpath=true&sortByEventpathIds=240%2C227%2C24158235%2C22895%2C23091%2C22942%2C102490%2C22962%2C22920%2C35454808%2C32415090%2C31938288%2C25914812%2C239%2C226%2C215%2C99917500%2C10199131%2C10399131%2C2500%2C249%2C250%2C1%2C3700%2C5000%2C1700%2C1250%2C3400%2C238%2C2700%2C22886%2C22889%2C3500%2C1600%2C237%2C1100%2C2100%2C22881%2C1300%2C50%2C22888%2C22878%2C22877%2C22884%2C3%2C1900%2C10399132%2C1200%2C1400%2C2900%2C2%2C10999130%2C1800%2C5%2C3300%2C10999126%2C10999125%2C10999127%2C4%2C10999123%2C6%2C10999124%2C10999129%2C10999128&page=1&eventsPerPage=70&l=en"
    return dafabetGetData(url, "ELP")
def dafabetPL1():
    url = "https://als.dafabet.com/xapi/rest/events?bettable=true&marketStatus=OPEN&periodType=PRE_MATCH&includeMarkets=true&includeHiddenOutcomes=true&includeHiddenMarkets=false&maxMarketPerEvent=100&lightWeightResponse=true&sportGroups=REGULAR&allBettableEvents=true&marketFilter=GAME&eventType=GAME&excludeMarketByOpponent=true&marketTypeIds=12%2C3021%2C13%2C3007%2C1%2C29%2C2101%2C2722&periodIds=100%2C102%2C232%2C233%2C234%2C11511&includeAdditional=false&additionalMarketTypeIds=479%2C110124%2C13004%2C13005%2C13000&additionalPeriodIds=100%2C102%2C232%2C234&sortMarketsByPriceDifference=true&includeLiveEvents=true&sportCodes=FOOT%2CTENN%2CBASK%2CBASE%2CVOLL%2CBADM%2CICEH%2CAMFB%2CRUGL%2CRUGU%2CTABL%2CSNOO%2CDART%2CCRIC%2CHAND%2CEFOT%2CEBSK%2CVICR%2CFUTS%2CBEVO&liveMarketStatus=OPEN%2CSUSPENDED&liveAboutToStart=true&liveExcludeLongTermSuspended=true&eventPathIds=138809&maxMarketsPerMarketType=1&sortByEventpath=true&sortByEventpathIds=240%2C227%2C24158235%2C22895%2C23091%2C22942%2C102490%2C22962%2C22920%2C35454808%2C32415090%2C31938288%2C25914812%2C239%2C226%2C215%2C99917500%2C10199131%2C10399131%2C2500%2C249%2C250%2C1%2C3700%2C5000%2C1700%2C1250%2C3400%2C238%2C2700%2C22886%2C22889%2C3500%2C1600%2C237%2C1100%2C2100%2C22881%2C1300%2C50%2C22888%2C22878%2C22877%2C22884%2C3%2C1900%2C10399132%2C1200%2C1400%2C2900%2C2%2C10999130%2C1800%2C5%2C3300%2C10999126%2C10999125%2C10999127%2C4%2C10999123%2C6%2C10999124%2C10999129%2C10999128&page=1&eventsPerPage=70&l=en"
    return dafabetGetData(url, "PL1")
def dafabetUSM():
    url = "https://als.dafabet.com/xapi/rest/events?bettable=true&marketStatus=OPEN&periodType=PRE_MATCH&includeMarkets=true&includeHiddenOutcomes=true&includeHiddenMarkets=false&maxMarketPerEvent=100&lightWeightResponse=true&sportGroups=REGULAR&allBettableEvents=true&marketFilter=GAME&eventType=GAME&excludeMarketByOpponent=true&marketTypeIds=12%2C3021%2C13%2C3007%2C1%2C29%2C2101%2C2722&periodIds=100%2C102%2C232%2C233%2C234%2C11511&includeAdditional=false&additionalMarketTypeIds=479%2C110124%2C13004%2C13005%2C13000&additionalPeriodIds=100%2C102%2C232%2C234&sortMarketsByPriceDifference=true&includeLiveEvents=true&sportCodes=FOOT%2CTENN%2CBASK%2CBASE%2CVOLL%2CBADM%2CICEH%2CAMFB%2CRUGL%2CRUGU%2CTABL%2CSNOO%2CDART%2CCRIC%2CHAND%2CEFOT%2CEBSK%2CVICR%2CFUTS%2CBEVO&liveMarketStatus=OPEN%2CSUSPENDED&liveAboutToStart=true&liveExcludeLongTermSuspended=true&eventPathIds=23115&maxMarketsPerMarketType=1&sortByEventpath=true&sortByEventpathIds=240%2C227%2C24158235%2C22895%2C23091%2C22942%2C102490%2C22962%2C22920%2C35454808%2C32415090%2C31938288%2C25914812%2C239%2C226%2C215%2C99917500%2C10199131%2C10399131%2C2500%2C249%2C250%2C1%2C3700%2C5000%2C1700%2C1250%2C3400%2C238%2C2700%2C22886%2C22889%2C3500%2C1600%2C237%2C1100%2C2100%2C22881%2C1300%2C50%2C22888%2C22878%2C22877%2C22884%2C3%2C1900%2C10399132%2C1200%2C1400%2C2900%2C2%2C10999130%2C1800%2C5%2C3300%2C10999126%2C10999125%2C10999127%2C4%2C10999123%2C6%2C10999124%2C10999129%2C10999128&page=1&eventsPerPage=70&l=en"
    return dafabetGetData(url, "USM")

def dafabetEPL():
    url = "https://als.dafabet.com/xapi/rest/events?bettable=true&marketStatus=OPEN&periodType=PRE_MATCH&includeMarkets=true&includeHiddenOutcomes=true&includeHiddenMarkets=false&maxMarketPerEvent=100&lightWeightResponse=true&sportGroups=REGULAR&allBettableEvents=true&marketFilter=GAME&eventType=GAME&excludeMarketByOpponent=true&marketTypeIds=1&periodIds=100%2C200%2C232%2C233&maxMarketsPerMarketType=100&sortMarketsByPriceDifference=true&includeLiveEvents=true&sportCodes=FOOT%2CTENN%2CBASK%2CBASE%2CVOLL%2CBADM%2CICEH%2CAMFB%2CRUGL%2CRUGU%2CTABL%2CSNOO%2CDART%2CCRIC%2CHAND%2CSQUA%2CEFOT%2CEBSK%2CVICR%2CFUTS%2CBEVO&liveMarketStatus=OPEN%2CSUSPENDED&liveAboutToStart=true&liveExcludeLongTermSuspended=true&eventPathIds=23132&sortByEventpath=true&sortByEventpathIds=240%2C227%2C24158235%2C22895%2C23091%2C22942%2C102490%2C22962%2C22920%2C35454808%2C32415090%2C31938288%2C25914812%2C239%2C226%2C215%2C99917500%2C10199131%2C10399131%2C2500%2C249%2C250%2C1%2C3700%2C5000%2C1700%2C1250%2C3400%2C238%2C2700%2C22886%2C22889%2C3500%2C1600%2C237%2C1100%2C2100%2C22881%2C1300%2C50%2C22888%2C22878%2C22877%2C22884%2C3%2C1900%2C10399132%2C1200%2C1400%2C2900%2C2%2C10999130%2C1800%2C5%2C3300%2C10999126%2C10999125%2C10999127%2C4%2C10999123%2C6%2C10999124%2C10999129%2C10999128&page=1&eventsPerPage=70&l=en"
    return dafabetGetData(url, "EPL")
def dafabetEL1():
    url = 'https://als.dafabet.com/xapi/rest/events?bettable=true&marketStatus=OPEN&periodType=PRE_MATCH&includeMarkets=true&includeHiddenOutcomes=true&includeHiddenMarkets=false&maxMarketPerEvent=100&lightWeightResponse=true&sportGroups=REGULAR&allBettableEvents=true&marketFilter=GAME&eventType=GAME&excludeMarketByOpponent=true&marketTypeIds=1&periodIds=100%2C200%2C232%2C233&maxMarketsPerMarketType=100&sortMarketsByPriceDifference=true&includeLiveEvents=true&sportCodes=FOOT%2CTENN%2CBASK%2CBASE%2CVOLL%2CBADM%2CICEH%2CAMFB%2CRUGL%2CRUGU%2CTABL%2CSNOO%2CDART%2CCRIC%2CHAND%2CSQUA%2CEFOT%2CEBSK%2CVICR%2CFUTS%2CBEVO&liveMarketStatus=OPEN%2CSUSPENDED&liveAboutToStart=true&liveExcludeLongTermSuspended=true&eventPathIds=23058&sortByEventpath=true&sortByEventpathIds=240%2C227%2C24158235%2C22895%2C23091%2C22942%2C102490%2C22962%2C22920%2C35454808%2C32415090%2C31938288%2C25914812%2C239%2C226%2C215%2C99917500%2C10199131%2C10399131%2C2500%2C249%2C250%2C1%2C3700%2C5000%2C1700%2C1250%2C3400%2C238%2C2700%2C22886%2C22889%2C3500%2C1600%2C237%2C1100%2C2100%2C22881%2C1300%2C50%2C22888%2C22878%2C22877%2C22884%2C3%2C1900%2C10399132%2C1200%2C1400%2C2900%2C2%2C10999130%2C1800%2C5%2C3300%2C10999126%2C10999125%2C10999127%2C4%2C10999123%2C6%2C10999124%2C10999129%2C10999128&page=1&eventsPerPage=70&l=en'
    return dafabetGetData(url, "EL1")
def dafabetEL2():
    url = 'https://als.dafabet.com/xapi/rest/events?bettable=true&marketStatus=OPEN&periodType=PRE_MATCH&includeMarkets=true&includeHiddenOutcomes=true&includeHiddenMarkets=false&maxMarketPerEvent=100&lightWeightResponse=true&sportGroups=REGULAR&allBettableEvents=true&marketFilter=GAME&eventType=GAME&excludeMarketByOpponent=true&marketTypeIds=1&periodIds=100%2C200%2C232%2C233&maxMarketsPerMarketType=100&sortMarketsByPriceDifference=true&includeLiveEvents=true&sportCodes=FOOT%2CTENN%2CBASK%2CBASE%2CVOLL%2CBADM%2CICEH%2CAMFB%2CRUGL%2CRUGU%2CTABL%2CSNOO%2CDART%2CCRIC%2CHAND%2CSQUA%2CEFOT%2CEBSK%2CVICR%2CFUTS%2CBEVO&liveMarketStatus=OPEN%2CSUSPENDED&liveAboutToStart=true&liveExcludeLongTermSuspended=true&eventPathIds=23522&sortByEventpath=true&sortByEventpathIds=240%2C227%2C24158235%2C22895%2C23091%2C22942%2C102490%2C22962%2C22920%2C35454808%2C32415090%2C31938288%2C25914812%2C239%2C226%2C215%2C99917500%2C10199131%2C10399131%2C2500%2C249%2C250%2C1%2C3700%2C5000%2C1700%2C1250%2C3400%2C238%2C2700%2C22886%2C22889%2C3500%2C1600%2C237%2C1100%2C2100%2C22881%2C1300%2C50%2C22888%2C22878%2C22877%2C22884%2C3%2C1900%2C10399132%2C1200%2C1400%2C2900%2C2%2C10999130%2C1800%2C5%2C3300%2C10999126%2C10999125%2C10999127%2C4%2C10999123%2C6%2C10999124%2C10999129%2C10999128&page=1&eventsPerPage=70&l=en'
    return dafabetGetData(url, "EL2")
def dafabetSP():
    url = 'https://als.dafabet.com/xapi/rest/events?bettable=true&marketStatus=OPEN&periodType=PRE_MATCH&includeMarkets=true&includeHiddenOutcomes=true&includeHiddenMarkets=false&maxMarketPerEvent=100&lightWeightResponse=true&sportGroups=REGULAR&allBettableEvents=true&marketFilter=GAME&eventType=GAME&excludeMarketByOpponent=true&marketTypeIds=1&periodIds=100%2C200%2C232%2C233&maxMarketsPerMarketType=100&sortMarketsByPriceDifference=true&includeLiveEvents=true&sportCodes=FOOT%2CTENN%2CBASK%2CBASE%2CVOLL%2CBADM%2CICEH%2CAMFB%2CRUGL%2CRUGU%2CTABL%2CSNOO%2CDART%2CCRIC%2CHAND%2CSQUA%2CEFOT%2CEBSK%2CVICR%2CFUTS%2CBEVO&liveMarketStatus=OPEN%2CSUSPENDED&liveAboutToStart=true&liveExcludeLongTermSuspended=true&eventPathIds=23309&sortByEventpath=true&sortByEventpathIds=240%2C227%2C24158235%2C22895%2C23091%2C22942%2C102490%2C22962%2C22920%2C35454808%2C32415090%2C31938288%2C25914812%2C239%2C226%2C215%2C99917500%2C10199131%2C10399131%2C2500%2C249%2C250%2C1%2C3700%2C5000%2C1700%2C1250%2C3400%2C238%2C2700%2C22886%2C22889%2C3500%2C1600%2C237%2C1100%2C2100%2C22881%2C1300%2C50%2C22888%2C22878%2C22877%2C22884%2C3%2C1900%2C10399132%2C1200%2C1400%2C2900%2C2%2C10999130%2C1800%2C5%2C3300%2C10999126%2C10999125%2C10999127%2C4%2C10999123%2C6%2C10999124%2C10999129%2C10999128&page=1&eventsPerPage=70&l=en'
    return dafabetGetData(url, "SP")
def dafabetSC():
    url = 'https://als.dafabet.com/xapi/rest/events?bettable=true&marketStatus=OPEN&periodType=PRE_MATCH&includeMarkets=true&includeHiddenOutcomes=true&includeHiddenMarkets=false&maxMarketPerEvent=100&lightWeightResponse=true&sportGroups=REGULAR&allBettableEvents=true&marketFilter=GAME&eventType=GAME&excludeMarketByOpponent=true&marketTypeIds=1&periodIds=100%2C200%2C232%2C233&maxMarketsPerMarketType=100&sortMarketsByPriceDifference=true&includeLiveEvents=true&sportCodes=FOOT%2CTENN%2CBASK%2CBASE%2CVOLL%2CBADM%2CICEH%2CAMFB%2CRUGL%2CRUGU%2CTABL%2CSNOO%2CDART%2CCRIC%2CHAND%2CSQUA%2CEFOT%2CEBSK%2CVICR%2CFUTS%2CBEVO&liveMarketStatus=OPEN%2CSUSPENDED&liveAboutToStart=true&liveExcludeLongTermSuspended=true&eventPathIds=23420&sortByEventpath=true&sortByEventpathIds=240%2C227%2C24158235%2C22895%2C23091%2C22942%2C102490%2C22962%2C22920%2C35454808%2C32415090%2C31938288%2C25914812%2C239%2C226%2C215%2C99917500%2C10199131%2C10399131%2C2500%2C249%2C250%2C1%2C3700%2C5000%2C1700%2C1250%2C3400%2C238%2C2700%2C22886%2C22889%2C3500%2C1600%2C237%2C1100%2C2100%2C22881%2C1300%2C50%2C22888%2C22878%2C22877%2C22884%2C3%2C1900%2C10399132%2C1200%2C1400%2C2900%2C2%2C10999130%2C1800%2C5%2C3300%2C10999126%2C10999125%2C10999127%2C4%2C10999123%2C6%2C10999124%2C10999129%2C10999128&page=1&eventsPerPage=70&l=en'
    return dafabetGetData(url, "SC")
def dafabetIFD():
    url = 'https://als.dafabet.com/xapi/rest/events?bettable=true&marketStatus=OPEN&periodType=PRE_MATCH&includeMarkets=true&includeHiddenOutcomes=true&includeHiddenMarkets=false&maxMarketPerEvent=100&lightWeightResponse=true&sportGroups=REGULAR&allBettableEvents=true&marketFilter=GAME&eventType=GAME&excludeMarketByOpponent=true&marketTypeIds=1&periodIds=100%2C200%2C232%2C233&maxMarketsPerMarketType=100&sortMarketsByPriceDifference=true&includeLiveEvents=true&sportCodes=FOOT%2CTENN%2CBASK%2CBASE%2CVOLL%2CBADM%2CICEH%2CAMFB%2CRUGL%2CRUGU%2CTABL%2CSNOO%2CDART%2CCRIC%2CHAND%2CSQUA%2CEFOT%2CEBSK%2CVICR%2CFUTS%2CBEVO&liveMarketStatus=OPEN%2CSUSPENDED&liveAboutToStart=true&liveExcludeLongTermSuspended=true&eventPathIds=25992&sortByEventpath=true&sortByEventpathIds=240%2C227%2C24158235%2C22895%2C23091%2C22942%2C102490%2C22962%2C22920%2C35454808%2C32415090%2C31938288%2C25914812%2C239%2C226%2C215%2C99917500%2C10199131%2C10399131%2C2500%2C249%2C250%2C1%2C3700%2C5000%2C1700%2C1250%2C3400%2C238%2C2700%2C22886%2C22889%2C3500%2C1600%2C237%2C1100%2C2100%2C22881%2C1300%2C50%2C22888%2C22878%2C22877%2C22884%2C3%2C1900%2C10399132%2C1200%2C1400%2C2900%2C2%2C10999130%2C1800%2C5%2C3300%2C10999126%2C10999125%2C10999127%2C4%2C10999123%2C6%2C10999124%2C10999129%2C10999128&page=1&eventsPerPage=70&l=en'
    return dafabetGetData(url, "IFD")
def dafabetIPD():
    url = 'https://als.dafabet.com/xapi/rest/events?bettable=true&marketStatus=OPEN&periodType=PRE_MATCH&includeMarkets=true&includeHiddenOutcomes=true&includeHiddenMarkets=false&maxMarketPerEvent=100&lightWeightResponse=true&sportGroups=REGULAR&allBettableEvents=true&marketFilter=GAME&eventType=GAME&excludeMarketByOpponent=true&marketTypeIds=1&periodIds=100%2C200%2C232%2C233&maxMarketsPerMarketType=100&sortMarketsByPriceDifference=true&includeLiveEvents=true&sportCodes=FOOT%2CTENN%2CBASK%2CBASE%2CVOLL%2CBADM%2CICEH%2CAMFB%2CRUGL%2CRUGU%2CTABL%2CSNOO%2CDART%2CCRIC%2CHAND%2CSQUA%2CEFOT%2CEBSK%2CVICR%2CFUTS%2CBEVO&liveMarketStatus=OPEN%2CSUSPENDED&liveAboutToStart=true&liveExcludeLongTermSuspended=true&eventPathIds=22916&sortByEventpath=true&sortByEventpathIds=240%2C227%2C24158235%2C22895%2C23091%2C22942%2C102490%2C22962%2C22920%2C35454808%2C32415090%2C31938288%2C25914812%2C239%2C226%2C215%2C99917500%2C10199131%2C10399131%2C2500%2C249%2C250%2C1%2C3700%2C5000%2C1700%2C1250%2C3400%2C238%2C2700%2C22886%2C22889%2C3500%2C1600%2C237%2C1100%2C2100%2C22881%2C1300%2C50%2C22888%2C22878%2C22877%2C22884%2C3%2C1900%2C10399132%2C1200%2C1400%2C2900%2C2%2C10999130%2C1800%2C5%2C3300%2C10999126%2C10999125%2C10999127%2C4%2C10999123%2C6%2C10999124%2C10999129%2C10999128&page=1&eventsPerPage=70&l=en'
    return dafabetGetData(url, "IPD")
def dafabetSPD():
    url = 'https://als.dafabet.com/xapi/rest/events?bettable=true&marketStatus=OPEN&periodType=PRE_MATCH&includeMarkets=true&includeHiddenOutcomes=true&includeHiddenMarkets=false&maxMarketPerEvent=100&lightWeightResponse=true&sportGroups=REGULAR&allBettableEvents=true&marketFilter=GAME&eventType=GAME&excludeMarketByOpponent=true&marketTypeIds=1&periodIds=100%2C200%2C232%2C233&maxMarketsPerMarketType=100&sortMarketsByPriceDifference=true&includeLiveEvents=true&sportCodes=FOOT%2CTENN%2CBASK%2CBASE%2CVOLL%2CBADM%2CICEH%2CAMFB%2CRUGL%2CRUGU%2CTABL%2CSNOO%2CDART%2CCRIC%2CHAND%2CSQUA%2CEFOT%2CEBSK%2CVICR%2CFUTS%2CBEVO&liveMarketStatus=OPEN%2CSUSPENDED&liveAboutToStart=true&liveExcludeLongTermSuspended=true&eventPathIds=23034&sortByEventpath=true&sortByEventpathIds=240%2C227%2C24158235%2C22895%2C23091%2C22942%2C102490%2C22962%2C22920%2C35454808%2C32415090%2C31938288%2C25914812%2C239%2C226%2C215%2C99917500%2C10199131%2C10399131%2C2500%2C249%2C250%2C1%2C3700%2C5000%2C1700%2C1250%2C3400%2C238%2C2700%2C22886%2C22889%2C3500%2C1600%2C237%2C1100%2C2100%2C22881%2C1300%2C50%2C22888%2C22878%2C22877%2C22884%2C3%2C1900%2C10399132%2C1200%2C1400%2C2900%2C2%2C10999130%2C1800%2C5%2C3300%2C10999126%2C10999125%2C10999127%2C4%2C10999123%2C6%2C10999124%2C10999129%2C10999128&page=1&eventsPerPage=70&l=en'
    return dafabetGetData(url, "SPD")
def dafabetSSD():
    url = 'https://als.dafabet.com/xapi/rest/events?bettable=true&marketStatus=OPEN&periodType=PRE_MATCH&includeMarkets=true&includeHiddenOutcomes=true&includeHiddenMarkets=false&maxMarketPerEvent=100&lightWeightResponse=true&sportGroups=REGULAR&allBettableEvents=true&marketFilter=GAME&eventType=GAME&excludeMarketByOpponent=true&marketTypeIds=1&periodIds=100%2C200%2C232%2C233&maxMarketsPerMarketType=100&sortMarketsByPriceDifference=true&includeLiveEvents=true&sportCodes=FOOT%2CTENN%2CBASK%2CBASE%2CVOLL%2CBADM%2CICEH%2CAMFB%2CRUGL%2CRUGU%2CTABL%2CSNOO%2CDART%2CCRIC%2CHAND%2CSQUA%2CEFOT%2CEBSK%2CVICR%2CFUTS%2CBEVO&liveMarketStatus=OPEN%2CSUSPENDED&liveAboutToStart=true&liveExcludeLongTermSuspended=true&eventPathIds=28571&sortByEventpath=true&sortByEventpathIds=240%2C227%2C24158235%2C22895%2C23091%2C22942%2C102490%2C22962%2C22920%2C35454808%2C32415090%2C31938288%2C25914812%2C239%2C226%2C215%2C99917500%2C10199131%2C10399131%2C2500%2C249%2C250%2C1%2C3700%2C5000%2C1700%2C1250%2C3400%2C238%2C2700%2C22886%2C22889%2C3500%2C1600%2C237%2C1100%2C2100%2C22881%2C1300%2C50%2C22888%2C22878%2C22877%2C22884%2C3%2C1900%2C10399132%2C1200%2C1400%2C2900%2C2%2C10999130%2C1800%2C5%2C3300%2C10999126%2C10999125%2C10999127%2C4%2C10999123%2C6%2C10999124%2C10999129%2C10999128&page=1&eventsPerPage=70&l=en'
    return dafabetGetData(url, "SSD")
def dafabetFL1():
    url = 'https://als.dafabet.com/xapi/rest/events?bettable=true&marketStatus=OPEN&periodType=PRE_MATCH&includeMarkets=true&includeHiddenOutcomes=true&includeHiddenMarkets=false&maxMarketPerEvent=100&lightWeightResponse=true&sportGroups=REGULAR&allBettableEvents=true&marketFilter=GAME&eventType=GAME&excludeMarketByOpponent=true&marketTypeIds=1&periodIds=100%2C200%2C232%2C233&maxMarketsPerMarketType=100&sortMarketsByPriceDifference=true&includeLiveEvents=true&sportCodes=FOOT%2CTENN%2CBASK%2CBASE%2CVOLL%2CBADM%2CICEH%2CAMFB%2CRUGL%2CRUGU%2CTABL%2CSNOO%2CDART%2CCRIC%2CHAND%2CSQUA%2CEFOT%2CEBSK%2CVICR%2CFUTS%2CBEVO&liveMarketStatus=OPEN%2CSUSPENDED&liveAboutToStart=true&liveExcludeLongTermSuspended=true&eventPathIds=23169&sortByEventpath=true&sortByEventpathIds=240%2C227%2C24158235%2C22895%2C23091%2C22942%2C102490%2C22962%2C22920%2C35454808%2C32415090%2C31938288%2C25914812%2C239%2C226%2C215%2C99917500%2C10199131%2C10399131%2C2500%2C249%2C250%2C1%2C3700%2C5000%2C1700%2C1250%2C3400%2C238%2C2700%2C22886%2C22889%2C3500%2C1600%2C237%2C1100%2C2100%2C22881%2C1300%2C50%2C22888%2C22878%2C22877%2C22884%2C3%2C1900%2C10399132%2C1200%2C1400%2C2900%2C2%2C10999130%2C1800%2C5%2C3300%2C10999126%2C10999125%2C10999127%2C4%2C10999123%2C6%2C10999124%2C10999129%2C10999128&page=1&eventsPerPage=70&l=en'
    return dafabetGetData(url, "FL1")
def dafabetFL2():
    url = 'https://als.dafabet.com/xapi/rest/events?bettable=true&marketStatus=OPEN&periodType=PRE_MATCH&includeMarkets=true&includeHiddenOutcomes=true&includeHiddenMarkets=false&maxMarketPerEvent=100&lightWeightResponse=true&sportGroups=REGULAR&allBettableEvents=true&marketFilter=GAME&eventType=GAME&excludeMarketByOpponent=true&marketTypeIds=1&periodIds=100%2C200%2C232%2C233&maxMarketsPerMarketType=100&sortMarketsByPriceDifference=true&includeLiveEvents=true&sportCodes=FOOT%2CTENN%2CBASK%2CBASE%2CVOLL%2CBADM%2CICEH%2CAMFB%2CRUGL%2CRUGU%2CTABL%2CSNOO%2CDART%2CCRIC%2CHAND%2CSQUA%2CEFOT%2CEBSK%2CVICR%2CFUTS%2CBEVO&liveMarketStatus=OPEN%2CSUSPENDED&liveAboutToStart=true&liveExcludeLongTermSuspended=true&eventPathIds=23428&sortByEventpath=true&sortByEventpathIds=240%2C227%2C24158235%2C22895%2C23091%2C22942%2C102490%2C22962%2C22920%2C35454808%2C32415090%2C31938288%2C25914812%2C239%2C226%2C215%2C99917500%2C10199131%2C10399131%2C2500%2C249%2C250%2C1%2C3700%2C5000%2C1700%2C1250%2C3400%2C238%2C2700%2C22886%2C22889%2C3500%2C1600%2C237%2C1100%2C2100%2C22881%2C1300%2C50%2C22888%2C22878%2C22877%2C22884%2C3%2C1900%2C10399132%2C1200%2C1400%2C2900%2C2%2C10999130%2C1800%2C5%2C3300%2C10999126%2C10999125%2C10999127%2C4%2C10999123%2C6%2C10999124%2C10999129%2C10999128&page=1&eventsPerPage=70&l=en'
    return dafabetGetData(url, "FL2")

def dafabetGetData(url, tag):
  urls = []
  matches = nu.make_request(url, headers)
  dafabet_dict = {"Name":"Dafabet", "Matches": []}
  if(matches):
    event_list = [event['id'] for event in matches]
    for event in event_list:
       urls.append(f"https://als.dafabet.com/xapi/rest/events/{event}?bettable=true&marketStatus=OPEN&periodType=PRE_MATCH&includeMarkets=true&lightWeightResponse=true&includeLiveEvents=true&maxMarketPerEvent=1000&l=en")
    responses = nu.fetch_data(urls, headers, proxy_type='https')
    dafabet_dict = dafabetExtractData(responses, tag)
  return dafabet_dict

def dafabetExtractData(responses, tag):
    matches = []
    last_match_name = ""
    for response in responses:
        match_data = []
        if(not response):
           continue
        try:
          match_data = response.json()
        except ValueError:
          print('Dafabet JSON Decoding Failed')
        if(not match_data):
           continue
        h_odd = 0
        a_odd = 0
        d_odd = 0
        name = match_data['description'].split(' vs ')
        name1 = name[0]
        name2 = name[1]
        name = f'{normalizeName(tag, name1)} - {normalizeName(tag, name2)}'
        for market in match_data['markets']:
            if(market['description'] == 'Win/Draw/Win' and market['period']['fullDescription'] == 'Regular Time' and len(market['outcomes']) == 3):
                h_odd = market['outcomes'][0]['consolidatedPrice']['currentPrice']['decimal']
                a_odd = market['outcomes'][2]['consolidatedPrice']['currentPrice']['decimal']
                d_odd = market['outcomes'][1]['consolidatedPrice']['currentPrice']['decimal']
            fh_m = get_odds(match_data, 'Win/Draw/Win', 'First Half', 3)
            ggng = get_odds(match_data, 'Both teams to score', 'Regular Time', 2)
            dnb = get_odds(match_data, 'Win Match - Draw No Bet', 'Regular Time', 2)
            dc = get_odds(match_data, 'Double Chance', 'Regular Time', 3)

            sh_m = get_odds(match_data, 'Win/Draw/Win', 'Second Half', 3)
            fh_ggng = get_odds(match_data, 'Both teams to score', 'First Half', 2)
            fh_dnb = get_odds(match_data, 'Win Match - Draw No Bet', 'First Half', 2)
            fg = get_odds(match_data, 'Team To Score 1st Goal', 'Regular Time', 3)
            fh_fg = get_odds(match_data, 'Team To Score 1st Goal', 'First Half', 3)
            odd_even = get_odds(match_data, 'Even/Odd Total Goals', 'Regular Time', 2)
            fh_odd_even = get_odds(match_data, 'Even/Odd Total Goals', 'First Half', 2)
            ltts = get_odds(match_data, 'Last Team To Score', 'Regular Time', 3) # Last Team to Score
                
        if(h_odd == 0 and a_odd == 0 and d_odd == 0):
           continue
        if(name != last_match_name): #avoid duplicate matches
            last_match_name = name
            match = Match(name=name, home_odd=h_odd, away_odd=a_odd, draw_odd=d_odd, ggng=ggng, dnb=dnb, fh1x2=fh_m, dc=dc, sh1x2=sh_m, 
                         fg=fg, fh_fg=fh_fg, fh_dnb=fh_dnb, fh_ggng=fh_ggng, odd_even=odd_even, fh_odd_even=fh_odd_even,
                         ltts=ltts)
            matches.append(match)
            
    dafabet_dict = {"Name":"Dafabet", "Matches": matches}
    return dafabet_dict

def get_odds(match_data, description, period, num_odds):
    odds = []
    for market in match_data['markets']:
        if (market['description'] == description and market['period']['fullDescription'] == period and len(market['outcomes']) == num_odds):
            odds = [outcome['consolidatedPrice']['currentPrice']['decimal'] for outcome in market['outcomes']]
            if(num_odds == 3):
                odds = [market['outcomes'][0]['consolidatedPrice']['currentPrice']['decimal'],
                        market['outcomes'][2]['consolidatedPrice']['currentPrice']['decimal'],
                        market['outcomes'][1]['consolidatedPrice']['currentPrice']['decimal']]
            if(description == 'Even/Odd Total Goals'):
                odds = [market['outcomes'][1]['consolidatedPrice']['currentPrice']['decimal'],
                        market['outcomes'][0]['consolidatedPrice']['currentPrice']['decimal']]
    return odds

def normalizeName(tag, team_name):
    normalization_functions = {
        "ALP": normalizeDafabetAPLTeamNames,
        "BSA": normalizeDafabetBSATeamNames,
        "BSB": normalizeDafabetBSBTeamNames,
        "CPA": normalizeDafabetCPATeamNames,
        "CPB": normalizeDafabetCPBTeamNames,
        "ELP": normalizeDafabetELPTeamNames,
        "PL1": normalizeDafabetPL1TeamNames,
        "USM": normalizeDafabetUSMTeamNames,
        'EPL': normalizeDafabetEPLTeamNames,
        'EL1': normalizeDafabetEL1TeamNames,
        'EL2': normalizeDafabetEL2TeamNames,
        'SP': normalizeDafabetSPTeamNames,
        'SC': normalizeDafabetSCTeamNames,
        'IFD': normalizeDafabetIFDTeamNames,
        'IPD': normalizeDafabetIPDTeamNames,
        'SPD': normalizeDafabetSPDTeamNames,
        'SSD': normalizeDafabetSSDTeamNames,
        'FL1': normalizeDafabetFL1TeamNames,
        'FL2': normalizeDafabetFL2TeamNames
    }

    return normalization_functions.get(tag, lambda x: x)(team_name)
def normalizeDafabetAPLTeamNames(team_name):
  correct_name = process.extractOne(team_name, Liga_Profesional)[0]
  return correct_name
def normalizeDafabetBSATeamNames(team_name):
  correct_name = process.extractOne(team_name, Brazil_Serie_A)[0]
  return correct_name
def normalizeDafabetBSBTeamNames(team_name):
  correct_name = process.extractOne(team_name, Brazil_Serie_B)[0]
  return correct_name
def normalizeDafabetCPATeamNames(team_name):
  correct_name = process.extractOne(team_name, Colombia_Primera_A)[0]
  return correct_name
def normalizeDafabetCPBTeamNames(team_name):
  correct_name = process.extractOne(team_name, Colombia_Primera_B)[0]
  return correct_name
def normalizeDafabetELPTeamNames(team_name):
  return process.extractOne(team_name, Ecuador_ProLiga)[0]
def normalizeDafabetPL1TeamNames(team_name):
  return process.extractOne(team_name, Peru_Liga1)[0]
def normalizeDafabetUSMTeamNames(team_name):
  if(team_name == "Saint Louis City SC"):
     return 'St. Louis'
  return process.extractOne(team_name, UnitedS_Major_League)[0]
def normalizeDafabetEPLTeamNames(team_name):
  return process.extractOne(team_name, English_Premier_League)[0]
def normalizeDafabetEL1TeamNames(team_name):
  return process.extractOne(team_name, English_League_One)[0]
def normalizeDafabetEL2TeamNames(team_name):
  return process.extractOne(team_name, English_League_Two)[0]
def normalizeDafabetSPTeamNames(team_name):
  return process.extractOne(team_name, Scotland_Premiership)[0]
def normalizeDafabetSCTeamNames(team_name):
  return process.extractOne(team_name, Scotland_Championship)[0]
def normalizeDafabetIFDTeamNames(team_name):
  return process.extractOne(team_name, Ireland_First_Division)[0]
def normalizeDafabetIPDTeamNames(team_name):
  return process.extractOne(team_name, Ireland_Premier_Division)[0]
def normalizeDafabetSPDTeamNames(team_name):
  return process.extractOne(team_name, Spain_Primera_Division)[0]
def normalizeDafabetSSDTeamNames(team_name):
  return process.extractOne(team_name, Spain_Segunda_Division)[0]
def normalizeDafabetFL1TeamNames(team_name):
  return process.extractOne(team_name, France_Ligue1)[0]
def normalizeDafabetFL2TeamNames(team_name):
  return process.extractOne(team_name, France_Ligue2)[0]

if __name__ == '__main__':
  dafabet_dict = dafabetEPL()
  pd.set_option('display.max_colwidth', None)
  dafabetdF = pd.DataFrame.from_dict(dafabet_dict)
  print(dafabetdF)