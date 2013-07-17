# -*- coding: utf-8 -*-

# Pixiv API
# modify from tweepy (https://github.com/tweepy/tweepy/)

import StringIO

def payload_to_list(payload):
	result = []
	offset = 0
	length = 0
	# replace "" to `
	tmp_payload = payload.replace("\"\"", "`").strip()
	while offset < len(tmp_payload):
		if (tmp_payload[offset] == "\""):		# ,"xxx",
			length = tmp_payload[offset+1:].find("\"")
			result.append(tmp_payload[offset+1:offset+1+length])
			offset = offset + length + 3
		elif (tmp_payload[offset] == ","):		# ,,
			result.append("")
			offset += 1
		else:
			raise Exception("[off:%d] '%s' error: %s" % (offset, tmp_payload[offset:offset+8], tmp_payload))
	return result

class Image(object):
	def __str__(self):
		return "authorId=%d, id=%d, title=%s, point=%d, mobileURL: %s" % (self.authorId, self.id, self.title, self.point, self.mobileURL)

class ImageParser(object):

	@classmethod
	def parse(self, payload):
		if len(payload.strip()) > 17:
			image_obj = Image()

			# from http://sourceforge.jp/projects/pxv/scm/svn/blobs/head/trunk/src/pxv/Image.java
			# illust_id, id, type, title, server, name, thumbnail,,, mobile,,, date, tags, use_tool, ranking, total, views, description,,,, unknow1, unknow2, user_name,, unknow3,,, head,
			try:
				data = payload_to_list(payload)

				image_obj.id = int(data[0])
				image_obj.authorId = int(data[1])
				image_obj.ext = data[2]
				image_obj.title = data[3]
				image_obj.server = data[4]
				image_obj.authorName = data[5]
				image_obj.thumbURL = data[6]
				image_obj.mobileURL = data[9]
				image_obj.date = data[12]
				image_obj.tags = data[13]
				image_obj.tool = data[14]
				image_obj.feedback = int(data[15])
				image_obj.point = int(data[16])
				image_obj.views = int(data[17])
				image_obj.comment = data[18]
				try:
					image_obj.pages = int(data[19])
				except ValueError, e:
					image_obj.pages = 0

				image_obj.url = "http://www.pixiv.net/member_illust.php?mode=medium&illust_id=%s" % image_obj.id
				base_url = image_obj.mobileURL[0:image_obj.mobileURL.rfind("/mobile/")+1]
				image_obj.imageURL = "%s%s.%s" % (base_url, image_obj.id, image_obj.ext)

				image_obj.pageURL = []
				if (image_obj.pages > 0):
					for i in range(image_obj.pages):
						image_obj.pageURL.append("%s%s_big_p%d.%s" % (base_url, image_obj.id, i, image_obj.ext))
				else:
					image_obj.pageURL.append(image_obj.imageURL)

			except Exception, e:
				raise Exception('Failed to unpack data: %s\n%s' % (e, payload))

			return image_obj

		else:	# payload maybe null
			return None


	@classmethod
	def parse_list(self, payload):
		finput = StringIO.StringIO(payload)
		result = []
		while True:
			line = finput.readline()
			if (not line): break
			result.append(self.parse(line))
		return result


class User(object):
	def __str__(self):
		return "authorId=%d, authorName=%s, username=%s, thumbURL: %s" % (self.authorId, self.authorName, self.username, self.thumbURL)

class UserParser(object):

	@classmethod
	def parse(self, payload):
		if len(payload.strip()) > 26:
			user_obj = User()

			# ,"428027",,,,"瑠奈璃亜","http://i1.pixiv.net/img21/profile/lunalia/mobile/2791844_58.jpg",,,,,,,,,,,,,,,,,,"lunalia",,
			try:
				data = payload_to_list(payload)

				user_obj.authorId = int(data[1])
				user_obj.authorName = data[5]
				user_obj.thumbURL = data[6]
				user_obj.username = data[24]

				user_obj.url = "http://www.pixiv.net/member.php?id=%s" % user_obj.authorId

			except Exception, e:
				raise Exception('Failed to unpack data: %s\n%s' % (e, payload))

			return user_obj

		else:	# payload maybe null
			return None


	@classmethod
	def parse_list(self, payload):
		finput = StringIO.StringIO(payload)
		result = []
		while True:
			line = finput.readline()
			if (not line): break
			result.append(self.parse(line))
		return result

