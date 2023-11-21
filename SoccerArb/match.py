class Match:
    def __init__(self, name, home_odd, away_odd, draw_odd = 0, over={}, under={}, dc=[], dnb=[], fh1x2=[], ggng=[], 
                 fh_dnb=[], fh_ggng=[], odd_even=[], fh_odd_even=[], fg=[], fh_fg=[], sh1x2=[], ltts=[], sh_dnb=[], sh_ggng=[]):  
        self.name = name
        self.home_odd = home_odd
        self.away_odd = away_odd
        self.draw_odd = draw_odd
        self.over = over
        self.under = under
        self.dc = dc
        self.dnb = dnb
        self.fh1x2 = fh1x2
        self.ggng = ggng

        self.sh1x2 = sh1x2 
        self.odd_even = odd_even
        self.fh_odd_even = fh_odd_even
        self.fg = fg
        self.fh_fg = fh_fg
        self.fh_dnb = fh_dnb
        self.fh_ggng = fh_ggng
        self.ltts = ltts
        self.sh_dnb = sh_dnb
        self.sh_ggng = sh_ggng
    def __repr__(self):
        return f"{self.name} | {self.home_odd}, {self.away_odd}, {self.draw_odd}, o={self.over} u={self.under} dnb={self.dnb} fh={self.fh1x2} gg={self.ggng} oe={self.odd_even} fg={self.fg} fhdnb={self.fh_dnb} fhggng={self.fh_ggng}, fhoe={self.fh_odd_even}, shm={self.sh1x2}"

class Arb:
    def __init__(self, book1, book2, odd1, odd2, roi, wager_type, home_team, away_team, league, odd3=0, line_h=0, line_a=0, book3=""):  
        self.book1 = book1
        self.book2 = book2
        self.book3 = book3
        self.home_team = home_team
        self.away_team = away_team
        self.odd1 = odd1
        self.odd2 = odd2
        self.odd3 = odd3
        self.roi = roi
        self.wager_type = wager_type
        self.league = league
        self.line_h = line_h
        self.line_a = line_a
    def __repr__(self):
        if(self.odd3 != 0):
            return f"{self.wager_type} - {self.book1} | {self.home_team} {self.odd1}, {self.book2} | {self.away_team} {self.odd2}, Highest X on {self.book3} {self.odd3}, ROI={self.roi}"
        return f"{self.wager_type} - {self.book1} | {self.home_team} {self.odd1}, {self.book2} | {self.away_team} {self.odd2}, ROI={self.roi}"
