import scrapy
import sys
sys.path.insert(0,':\\Users\\47483\\Documents\\ForumScraper\\forum\\forum')

print(sys.path)
import datetime
from calendar import monthrange

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

"""
tickers = ['AASB','ABG', ADE,ADS,AEGA,AFG,AGLX,AIRX,AKAST,AKER,AKBM,AKRBP,ACC,ACH,AKH,AOW,AKSO,AKOBO,AKVA,
    ALT,AMSC,ANDF,ANORA,ABT,AQUA,ARCH,ABS,AFISH,AZT,AFK,ARGEO,ARR,ASTK,ASTRO,ATEA,ASA,AURA,AURG,AUSS,AUTO,AGAS,AWDR,
    ALNG,ACR,AYFIE,B2H,BAKKA,BALT,BARRA,BELCO,BCS,BGBIO,BEWI,BFISH,BSP,BONHR,BOR,BORR,BRG,BOUV,BRA,BWE,BWEK,BWIDL,BWLPG,
    BWO,BMA,CADLR,CAMBI,CARA,CARBN,CIRCA,CSS,CLOUD,CAPSL,CONTX,CRAYN,CSAM,CYVIZ,DVD,DSRT,DLTX,DNB,DNO,DOF,EAM,ECIT,ECO,
    EWIND,EIOF,EMGS,ELIMP,ELK,ELABS,ELOP,ELO,ENDUR,ENSU,ENTRA,ENVIP,EQNR,EPR,EFUEL,EXTX,FKRFT,FLNG,FLYR,FRO,FROY,GIG,
    RISH,GENT,GIGA,GJF,GNP,GEOS,GOGL,GOD,GEM,GSF,GRONG,GYL,HAFNI,HMONY,HAV,HKY,HAVI,HYARD,HEX,HPUR,HAUTO,HBC,HRGI,HOC,
    HUDL,HDLY,HUNT,HYPRO,HYN,HSPG,IFISH,ICEGR,ISLAX,IDEX,INDCT,INSR,INSTA,IWS,IOX,ITERA,JIN,JAREN,KAHOT,KAL,KID,KIT,KCC,
    KMCP,KOMPL,KOMP,KOA,KOG,KRAB,KYOTO,LSG,LIFE,LINK,LYTIX,MVW,MGN,MSEIS,MAS,MEDI,MELG,MWTR,MRCEL,MNTR,MOWI,MPCC,MPCES,
    MULTI,NAPA,NAVA,NKR,NEL,NOC,NEXT,NISB,NORBT,NCOD,NORDH,NOAP,NOHAL,NOM,NANOV,NOD,NUMND,NORSE,NHY,NSOL,NTI,NSKOG,NTEL,
    NORTH,NODL,NOL,NRS,NAS,NBX,NOR,NRC,NTS,NYKD,OBSRV,OSUN,OCY,OTS,ODL,ODF,ODFB,OKEA,OET,OLT,ORK,OTEC,OTOVO,PEN,PARB,
    PSKY,PCIB,PSE,PNOR,PEXIP,PGS,PHLY,PHO,PPG,PMG,POL,PLT,PRS,PROT,PROXI,PRYME,PYRUM,QFR,QFUEL,QUEST,QEC,R8P,RAKP,RANA,
    REACH,RECSI,RIVER,ROMER,ROM,ROMSB,SAGA,SALM,SALME,SACAM,SADG,SASNO,SATS,SBANK,SCANA,SCATC,SCHA,SCHB,SDSD,GEG,SDRL,
    SEAW7,SSG,SBO,SHLF,SIOFF,SIKRI,SKAND,SKI,SKUE,SMCRT,SMOP,SOFTX,SOGN,SOLON,SOFF,SOHO,SB68,MING,SRBNK,SOON,MORG,SOR,
    SVEG,SPOG,SNOR,SPOL,HELG,NONG,RING,SOAG,STATT,SNI,STB,STRO,SUBC,SUNSB,TRVX,TECH,TECO,TEKNA,TEL,TGS,KING,TIETO,TOM,
    TOTG,TRE,TYSB,ULTI,VEI,VISTN,VOLUE,VVL,VOW,VGM,WAWI,WSTEP,WEST,WWI,WWIB,WILS,XPLRA,XXL,YAR,ZAL,ZAP,ZENA,ZWIPE,ORN]
"""

test_tickers = ['ELOP', 'RECSI', 'KAHOOT' ]

def calculateDay(time):
    today = str(time.day)+'.'+str(time.month)+'.'+str(time.year)
    if (time.day - 1) == 0:
        yesterday = str(monthrange(time.year,time.month-1)[1])+'.'+str(time.month - 1)+'.'+str(time.year)
    else:
        yesterday = str(time.day-1) + '.' + str(time.month) + '.' + str(time.year)
    return today, yesterday

class Finansavisen(scrapy.Spider):
    name = "views"
    start_urls = ['https://finansavisen.no/forum/ticker/' + str(name) for name in test_tickers]

    #Finding todays and yesterdays dates
    today, yesterday = calculateDay(datetime.datetime.now().date())

    def parse(self, response):
        TABLE_SELECTOR = ".table"
        for reply in response.css(TABLE_SELECTOR):
            TICKER = '//tbody[@data-date = "' + self.today + '"]/tr/td[@class = "thread-ticker text-left"]/a/text()'
            THREAD_KEY_TODAY = '//tbody[@data-date = "' + self.today + '"]/tr/td[@class = "pl-0 w-100 ellipsis "]/a/@href'
            THREAD_KEY_YESTERDAY = '//tbody[@data-date = "' + self.yesterday + '"]/tr/td[@class = "pl-0 w-100 ellipsis "]/a/@href'
            REPLIES_TODAY = '//tbody[@data-date = "' + self.today + '"]/tr/td[@class = "text-right"]/a/text()'
            REPLIES_YESTERDAY = '//tbody[@data-date = "' + self.yesterday + '"]/tr/td[@class = "text-right"]/a/text()'
            VIEWS_TODAY = '//tbody[@data-date = "' + self.today + '"]/tr/td[@class = "hidden-sm-down text-right"]/text()'
            VIEWS_YESTERDAY = '//tbody[@data-date = "' + self.yesterday + '"]/tr/td[@class = "hidden-sm-down text-right"]/text()'
            item = ForumscannerItem()
            
            item['TICKER'] = reply.xpath(TICKER).extract_first().strip()
            item['THREAD_KEY_TODAY'] = reply.xpath(THREAD_KEY_TODAY).extract()
            item['THREAD_KEY_YESTERDAY'] = reply.xpath(THREAD_KEY_YESTERDAY).getall()
            item['REPLIES_TODAY'] =reply.xpath(REPLIES_TODAY).getall()
            item['REPLIES_YESTERDAY']= reply.xpath(REPLIES_YESTERDAY).getall()
            item['VIEWS_TODAY']= reply.xpath(VIEWS_TODAY).getall()
            item['VIEWS_YESTERDAY']= reply.xpath(VIEWS_YESTERDAY).getall()
            yield item

class DNOmsetning(scrapy.Spider):
    """
    Finme aksjene sortert etter høyest omsetning
    """
    name = "omsetning"
    start_urls = ['https://investor.dn.no/#!/Utforsk/HoyOmsetning/OSE']

    def parse(self, response):
        TABLE_SELECTOR = ".table"
        for omsetning in response.css(TABLE_SELECTOR):
            TICKER_NAME = omsetning.xpath('tbody[@class="section-box"]/tr/td/a/text()').extract()
            yield {
            'ticker' : TICKER_NAME
            }
class Xtrainvestor(scrapy.Spider):
    pass

"""configure_logging()
runner = CrawlerRunner()
runner.crawl(ViewsSpider)
d = runner.join()
d.addBoth(lambda _: reactor.stop())
reactor.run()"""
