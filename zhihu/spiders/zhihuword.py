# -*- coding: utf-8 -*-
import json

import scrapy

from zhihu.items import QuestionItem, AnswerItem
from zhihu.tools import MongoTools


class ZhihuwordSpider(scrapy.Spider):
    name = 'zhihuword'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    # 采集问题url
    question_url = 'https://www.zhihu.com/api/v4/members/{}/questions?include={}&offset={}&limit=20'
    # 采集答案url
    answer_url = 'https://www.zhihu.com/api/v4/members/{}/answers?include={}&offset={}&limit=20&sort_by=created'
    url_token = ''
    q_include = 'data[*].created,answer_count,follower_count,author,admin_closed_comment'
    a_include = 'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,collapsed_by,suggest_edit,comment_count,can_comment,content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,review_info,question,excerpt,relationship.is_authorized,voting,is_author,is_thanked,is_nothelp;data[*].author.badge[?(type=best_answerer)].topic'

    def start_requests(self):
        # MongoTools.get_collect_task()
        token = 'liaoxuefeng'
        self.url_token = token
        yield scrapy.Request(url=self.question_url.format(token, self.q_include, 0), callback=self.parse_question)
        yield scrapy.Request(url=self.answer_url.format(token, self.a_include, 0), callback=self.parse_answer)

    '''爬取问题'''

    def parse_question(self, response):
        res = json.loads(response.text)
        if 'data' in res.keys():
            for question in res.get('data'):
                item = QuestionItem()
                for field in item.fields:
                    if field in question.keys():
                        item[field] = question.get(field)
                    item['url_token'] = self.url_token
                yield item
        if 'paging' in res.keys() and res.get('paging').get('is_end') is False:
            next_page = res.get('paging').get('next').replace('com/', 'com/api/v4/')
            yield scrapy.Request(next_page, callback=self.parse_question)

    '''爬取回答'''

    def parse_answer(self, response):
        res = json.loads(response.text)
        if 'data' in res.keys():
            for answer in res.get('data'):
                item = AnswerItem()
                for field in item.fields:
                    if field in answer.keys():
                        item[field] = answer.get(field)
                    item['url_token'] = self.url_token
                yield item
        if 'paging' in res.keys() and res.get('paging').get('is_end') is False:
            next_page = res.get('paging').get('next').replace('com/', 'com/api/v4/')
            yield scrapy.Request(next_page, callback=self.parse_answer)
