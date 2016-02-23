import wx
from wx.lib import scrolledpanel
import datetime
import sqlite3
from . import store
from . import parser
import textwrap


class MyFrame(wx.Frame):
    def __init__(self, *args1, **args2):
        super().__init__(*args1, **args2)
        typelist = ['不限', '爱情', '喜剧', '动画', '科幻', '动作', '悬疑',
        '犯罪', '惊悚', '文艺', '青春', '魔幻', '励志', '黑色幽默', '传记']
        nowyear = datetime.date.today().year
        yearlist = [str(x) for x in range(nowyear, 1959, -1)]
        yearlist.insert(0, '不限')
        self.selected = []
        self.font1 = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.font2 = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT)
        self.font3 = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        panel = wx.Panel(self)

        self.movielist = MoviePanel(panel, size=(595, 630), pos=(5, 80))

        self.yearcombo = wx.ComboBox(panel, pos=(60, 10), size=(70, 25), choices=yearlist)
        wx.StaticText(panel, -1, "年份", pos=(20, 10))

        self.getdata = wx.Button(panel, label="获取数据", pos=(140, 10), size=(70, 20))

        self.countrytext = wx.TextCtrl(panel, pos=(260, 10), size=(100, 20), value='不限')
        wx.StaticText(panel, -1, "国家", pos=(220, 10))

        self.typecombo = wx.ComboBox(panel, pos=(410, 10), size=(70, 25), choices=typelist)
        wx.StaticText(panel, -1, "类型", pos=(370, 10))

        self.stafftext = wx.TextCtrl(panel, pos=(100, 40), size=(100, 20), value='不限')
        wx.StaticText(panel, -1, "导演／主演", pos=(20, 40))

        self.filtercheck = wx.CheckBox(panel, label="只显示未看", pos=(220, 40))
        self.submit = wx.Button(panel, label="查询", pos=(320, 40), size=(50, 20))
        self.delete = wx.Button(panel, label="删除", pos=(380, 40), size=(50, 20))
        self.mark = wx.Button(panel, label="标记为已看", pos=(440, 40), size=(90, 20))

        self.submit.Bind(wx.EVT_BUTTON, self.getfromdb)
        self.getdata.Bind(wx.EVT_BUTTON, self.getfromdouban)
        self.delete.Bind(wx.EVT_BUTTON, self.deletefromdb)
        self.mark.Bind(wx.EVT_BUTTON, self.addselected)

        self.getfromdb()

    def getfromdb(self, event=None):
        year = self.yearcombo.GetStringSelection()
        country = self.countrytext.GetValue()
        movietype = self.typecombo.GetStringSelection()
        staff = self.stafftext.GetValue()
        notseen = self.filtercheck.IsChecked()

        self.movielist.DestroyChildren()

        conn = sqlite3.connect('movies.db')
        curs = conn.cursor()
        query = 'select * from Movies'
        queryapp = []

        if year != '不限':
            queryapp.append('year=%s' % year)
        if country != '不限':
            queryapp.append('info like "%' + country + '%"')
        if movietype != '不限':
            queryapp.append('info like "%' + movietype + '%"')
        if staff != '不限':
            queryapp.append('info like "%' + staff + '%"')
        if notseen:
            queryapp.append('seen=0')

        if len(queryapp):
            query = query + ' where ' + queryapp[0]
            if len(queryapp) == 1:
                pass
            else:
                for i in range(1, len(queryapp)):
                    query = query + ' and ' + queryapp[i]
        query += ' order by rating desc'
        curs.execute(query)
        for row in curs.fetchall():
            if row[2]:
                moviename = row[1] + ' / ' + row[2] + '  ' + str(row[4])
            else:
                moviename = row[1] + '  ' + str(row[4])
            cb = wx.CheckBox(self.movielist, row[0], moviename)
            cb.Bind(wx.EVT_CHECKBOX, self.selectedapp)
            cb.SetFont(self.font1)
            seen = wx.StaticText(self.movielist, -1, '')
            if row[7]:
                seen = wx.StaticText(self.movielist, -1, '已看')
            seen.SetFont(self.font3)
            seen.SetForegroundColour(wx.Colour(0, 100, 255))
            hbox = wx.BoxSizer()
            hbox.Add(cb, 0, wx.ALL, 5)
            hbox.Add(seen, 0, wx.ALL, 5)
            info = textwrap.fill(row[3], width=65)
            infotext = wx.StaticText(self.movielist, -1, info)
            infotext.SetFont(self.font2)
            self.movielist.sizer.Add(hbox, 0, wx.ALL, 5)
            self.movielist.sizer.Add(infotext, 0, wx.ALL, 5)
            self.movielist.sizer.Add(wx.StaticLine(self.movielist, -1, size=(580, -1)), 0, wx.ALL, 5)
        self.movielist.SetSizer(self.movielist.sizer)
        self.movielist.SetupScrolling()
        self.selected = []
        conn.commit()
        conn.close()

    def getfromdouban(self, event):
        year = self.yearcombo.GetStringSelection()
        if year == '不限':
            wx.MessageBox('Please choose a year.', caption='Tip')
            return
        try:
            store.store(parser.getdata(year), year)
        except:
            wx.MessageBox('Please make sure Internet connected.', caption='Tip')
            return
        self.getfromdb()

    def selectedapp(self, event):
        movieID = event.GetEventObject().GetId()
        self.selected.append(movieID)

    def addselected(self, event):
        if len(self.selected):
            conn = sqlite3.connect('movies.db')
            curs = conn.cursor()
            if len(self.selected) > 1:
                query = "UPDATE Movies SET seen=1 WHERE id in %s" % str(tuple(self.selected))
            else:
                query = "UPDATE Movies SET seen=1 WHERE id=%d" % self.selected[0]
            curs.execute(query)
            conn.commit()
            conn.close()
            self.selected = []
            self.getfromdb()

    def deletefromdb(self, event):
        if len(self.selected):
            conn = sqlite3.connect('movies.db')
            curs = conn.cursor()
            if len(self.selected) > 1:
                query = "DELETE FROM Movies WHERE id in %s" % str(tuple(self.selected))
            else:
                query = "DELETE FROM Movies WHERE id=%d" % self.selected[0]
            curs.execute(query)
            conn.commit()
            conn.close()
            self.selected = []
            self.getfromdb()


class MoviePanel(scrolledpanel.ScrolledPanel):
    def __init__(self, *args1, **args2):
        super().__init__(*args1, **args2)
        self.sizer = wx.BoxSizer(wx.VERTICAL)


app = wx.App()
mywin = MyFrame(None, title='Movie List', size=(600, 720), pos=(200, 20))
mywin.SetMaxSize((620, 750))
mywin.Show()
app.MainLoop()
