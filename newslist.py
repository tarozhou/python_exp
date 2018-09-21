#! usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from home_application.Util.TimeUtil import *
import urllib



class ADNewsListp0(list):
    def __init__(self, *args, **kwargs):
        super(ADNewsListp0, self).__init__(args[0])

    def _distinct_(self):
        '''
        添加去重逻辑
        :return:
        '''
        dict1 = {}
        arr = ADNewsListp0(list())
        for x in self:
            if (x.idocid not in dict1):
                dict1[x.idocid] = 1
                arr.append(x)
        return ADNewsListp0(arr)

    def _diff_(self, col):
        dictp1 = {}
        for x in col:
            dictp1[x.idocid] = x
        return ADNewsListp0([x for x in self if x.idocid not in dictp1])

    def _intersection(self,col):
        dictp1 = {}
        for x in col:
            dictp1[x.idocid] = x
        return ADNewsListp0([x for x in self if x.idocid in dictp1])

    def _to_output_(self):
        return "+".join([x.idocid + ":" + str(x.isnews) for x in self])

    def _extend_(self, col):
        self.extend(col)
        return self

    def length(self):
        return len(self)

    def _to_dict_(self):
        dictp0 = []
        for x in self:
            doct = {}
            doct['docid'] = str(x.idocid)
            doct['id'] = str(x.idocid)
            doct['type'] = str(x.istop)
            doct['doc_type'] = str(x.isnews)
            dictp0.append(doct)
        return dictp0

    def _to_dict_allinfo_(self):
        dictp0 = {}
        for x in self:
            dictp0[x.idocid] = x
        return dictp0

    def _to_dict_tt_(self):
        dictp0 = []
        for x in self:
            doct = {}
            doct['id'] = str(x.idocid)
            doct['type'] = str(x.isnews)
            doct['category']=str(x.cateIndex)
            doct['title'] = urllib.unquote(x.stitle)
            doct['screated'] = str(from_unixtime(x.sidxtime))
            doct['rcscore'] = str(x.lrscore)
            doct['ctr']=str(x.clickrate)
            doct['recmethod']=str(x.recmethod)
            doct['memo']=str(x.recmethod)
            doct['is_not_community']=str(x.is_not_community)
            dictp0.append(doct)
        return dictp0

    def _to_dict_fortest_(self):
        dictp0 = []
        for x in self:
            doct = {}
            doct['id'] = str(x.idocid)
            doct['isnews'] = str(x.isnews)
            doct['title'] = urllib.unquote(x.stitle)
            doct['screated'] = str(from_unixtime(x.sidxtime))
            doct['ctr'] = str(x.clickrate)
            doct['tagIndex'] = str(x.tagIndex)
            doct['cateIndex'] = str(x.cateIndex)
            dictp0.append(doct)
        return dictp0

    def _take_(self, n):
        return ADNewsListp0(self[0:n])

    def _getdocids_(self):
        return [x.idocid for x in self]

    def _getbytime_(self, starttime, endtime=None):
        endtime = endtime or int(time.time())
        return ADNewsListp0([x for x in self if (x.sidxtime >= starttime and x.sidxtime <= endtime)])

    def _getbycates_(self, icate):
        return ADNewsListp0([x for x in self if (x.cateIndex == icate)])

    def _getbydocids_(self, docids):
        docmap = self._to_dict_allinfo_()
        return ADNewsListp0([docmap[docid] for docid in docids if docid in docmap])

    def _getbyisnews_(self, isnews):
        return ADNewsListp0([x for x in self if (x.isnews == isnews)])

    def _merge_(self, other):
        return ADNewsListp0(list(set(self._extend_(other))))

    def _sortbyctr1_(self):

        return ADNewsListp0(sorted(self, key=lambda news: news.clickrate, reverse=True))

    def _sortbyctr_(self):
        '''
        按照新闻点击率排序
        :return:排序后的列表
        '''
        return sorted(self, key=lambda news: news.clickrate, reverse=True)

    def _sortbylrscore_(self):
        '''
        按照新闻点击率排序
        :return:排序后的列表
        '''
        return ADNewsListp0(sorted(self, key=lambda news: news.lrscore, reverse=True))

    def _sortbytime_(self):
        '''
        按照新闻时间排序
        :return:排序后的列表
        '''
        return sorted(self, key=lambda news: news.sidxtime, reverse=True)

    def _sortbytimesec_p0_(self):
        '''
        按照时间分桶排序
        :return: 排序后的结果
        '''
        sec1 = self._getbytime_(get_hours_before(24))._sortbyctr_()
        sec2 = self._getbytime_(get_hours_before(72))._diff_(sec1)._sortbyctr_()
        sec3 = self._diff_(sec1)._diff_(sec2)._sortbyctr_()
        return sec1 + sec2 + sec3

    def _sortbytimesec_p1_(self, itime=None):
        itime = itime or int(time.time())
        lingchen = getlingchentime(itime)
        yestd = get_hours_before(24, lingchen)
        thrd = get_hours_before(72, lingchen)
        sec0 = self._getbytime_(lingchen)._sortbyctr_()
        sec1 = self._getbytime_(yestd, lingchen)._sortbyctr_()
        sec2 = self._getbytime_(thrd, yestd)._sortbyctr_()
        sec3 = self._diff_(sec0)._diff_(sec1)._diff_(sec2)._sortbyctr_()
        return sec0 + sec1 + sec2 + sec3

    def _sortbytimesec_p2_(self, itime=None):
        itime = itime or int(time.time())
        lingchen = getlingchentime(itime)
        yestd = get_hours_before(24, lingchen)
        thrd = get_hours_before(72, lingchen)
        sec0 = self._getbytime_(lingchen)._sortbylrscore_()
        sec1 = self._getbytime_(yestd, lingchen)._sortbylrscore_()
        sec2 = self._getbytime_(thrd, yestd)._sortbylrscore_()
        sec3 = self._diff_(sec0)._diff_(sec1)._diff_(sec2)._sortbylrscore_()
        return sec0 + sec1 + sec2 + sec3

    def _setvideocates_(self):
        '''
        设置为视频类别
        :return: 视频
        '''
        for item in self:
            if (item.isnews == 1):
                item.__setattr__("cateIndex", 10)

    def _set_is_not_community_(self,is_not_community="0"):
        for item in self:
            item.__setattr__("is_not_community", is_not_community)

    def _setLRscore_(self, docid_score):
        '''
        fill in the lrscore
        :return: news list
        '''
        for item in self:
            if (item.idocid in docid_score):
                item.__setattr__("lrscore", docid_score[item.idocid])

    def _setProperty_(self, property_name,docid_property):
        '''
        fill in the lrscore
        :return: news list
        '''
        for item in self:
            if (item.idocid in docid_property):
                item.__setattr__(property_name, docid_property[item.idocid])

    def _getcates_(self):
        '''
        获取新闻类别
        :return: 新闻类别array
        '''
        return sorted(list(set([x.cateIndex for x in self])))

    def _getnewsbycate_(self, cateid):
        '''
        根据新闻类别获取新闻
        :param cateid:类别
        :return:新闻列表
        '''
        return ADNewsListp0([x for x in self if x.cateIndex == cateid])

    def _getnewsbyrecall_(self,recall_method):

        return ADNewsListp0([x for x in self if x.recmethod == recall_method])

    def _filternewsbytype_(self, cateid):
        '''
        根据新闻类别过滤掉新闻
        :param cateid:3
        :return:None
        '''
        return ADNewsListp0([x for x in self if x.cateIndex != cateid])

    def _deleteredundantvideo_(self,remainnum=1):
        '''
        1.视频条数
            如果总条数大于20，可以保留3条
            如果总条数小于20，只有1条

            最后检查：如果总条数小于5，不要视频
        2.视频位置 TODO
            两个视频不能同时出现
        :return:none
        '''

        def _remove_(remainnum):
            i = 0
            p = 0
            while i < len(self):
                if self[i].isnews == 1:
                    p += 1
                if p > remainnum:
                    del (self[i])
                    p -= 1
                    i -= 1
                i += 1

        _remove_(3) if len(self) > 20 else _remove_(remainnum)
        '''
        if len(self) > 20:
            _remove_(3)
        elif len(self)>5:
            _remove_(1)
        else:
            _remove_(0)
        '''
        if len(self) < 5:
            _remove_(0)

    def _resetmryx_(self):
        '''
        把每日一笑提前
        :return:
        '''
        mryx = self._getbycates_(4)
        if len(mryx) > 0:
            self.remove(mryx[0])
            self.insert(0, mryx[0])

    def _resetvideo_(self):
        '''
        如果前四位出现视频，把视频移到最后的位置
        :return:
        '''
        video = self._take_(4)._getbyisnews_(1)
        if len(video) > 0:
            self.remove(video[0])
            self.append(video[0])


class newsInfop0(object):
    def __init__(self, idocid="",
                 isourceid=0,
                 tagIndex="",
                 cateIndex=0,
                 isnews=0,
                 sidxtime=0,
                 stitle="",
                 clickrate=0.0,
                 lrscore=0.0,
                 istop=0,
                 stagids="",
                 ssource="",
                 recmethod="",
                 is_not_community="0",
                 totalscore=0.0
                 ):
        self.idocid = idocid
        self.isourceid = isourceid
        self.tagIndex = tagIndex
        self.cateIndex = cateIndex
        self.sidxtime = sidxtime
        self.stagids = stagids
        self.stitle = stitle
        self.isnews = isnews
        self.clickrate = clickrate
        self.lrscore = lrscore
        self.istop = istop
        self.ssoucre = ssource
        self.recmethod = recmethod
        self.is_not_community=is_not_community
        self.totalscore=totalscore

    def __str__(self):
        return self.idocid + ":" + str(self.isnews)

    def __repr__(self):
        return self.idocid + ":" + str(self.isnews) + ":" + str(self.cateIndex)
