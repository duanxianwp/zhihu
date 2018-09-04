# -*- coding: utf-8 -*-
import json

import scrapy

from zhihu.items import UserItem
from zhihu.tools import MongoTools


class ZhihuuserSpider(scrapy.Spider):
    name = 'zhihuuser'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    # 获取详细信息
    user_query = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,answer_count,articles_count,pins_count,question_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'
    url_user = 'https://www.zhihu.com/api/v4/members/{token}?include={include}'
    # 获取关注列表
    followee_query = 'data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
    url_followee = 'https://www.zhihu.com/api/v4/members/{token}/followees?include={include}&offset={offset}&limit={limit}'
    # 获取粉丝列表
    follower_query = 'data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
    url_follower = 'https://www.zhihu.com/api/v4/members/{token}/followers?include={include}&offset={offset}&limit={limit}'

    def start_requests(self):
        token = 'liaoxuefeng'
        yield scrapy.Request(url=self.url_user.format(token=token, include=self.user_query),
                             callback=self.parse_user_info)

    def parse_user_info(self, response):
        result = json.loads(response.text)
        item = UserItem()
        for field in item.fields:
            if field in result.keys():
                item[field] = result.get(field)
        yield item
        yield scrapy.Request(
            url=self.url_followee.format(token=result.get('url_token'), include=self.followee_query, offset=0,
                                         limit=20),
            callback=self.parse_follows)
        yield scrapy.Request(
            url=self.url_follower.format(token=result.get('url_token'), include=self.follower_query, offset=0,
                                         limit=20),
            callback=self.parse_follows)

    def parse_follows(self, response):
        res = json.loads(response.text)
        if 'data' in res.keys():
            for result in res.get('data'):
                token = result.get('url_token')
                # 如果这个人在库里已经有了就不再进行深度扫描
                if not MongoTools.query_item(token):
                    yield scrapy.Request(url=self.url_user.format(token=token, include=self.user_query),
                                         callback=self.parse_user_info)
        if 'paging' in res.keys() and res.get('paging').get('is_end') is False:
            next_page = res.get('paging').get('next')
            yield scrapy.Request(next_page, callback=self.parse_follows)
