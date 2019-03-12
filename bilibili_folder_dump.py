#!/usr/bin/python3
import os
import json
import requests
# import ffmpeg

# f_cookies = open(r"./myBilibiliCookies.txt","r")
# cookies = f_cookies.read()
# f_cookies.close()

# headers = {
#     'Accept':'application/json, text/plain, text/plain;charset=UTF-8, */*',
# #     'Accept-Encoding':'gzip, deflate, br',
# #     'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
# #     'Connection':'keep-alive',
#     'Cookie': cookies,
# #     'Host':'space.bilibili.com',
# #     'Origin':'https://space.bilibili.com',
# #     'Referer':'https://space.bilibili.com/uid/favlist?fid=',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
# }       

prefix = 'https://api.bilibili.com/medialist/gateway/base/'

medialist_brief = []

def all_info_dump():
	mid = input('User ID (aka uid/mid): ')

	medialist_brief_jsonp = prefix + 'created?pn=1&ps=100&up_mid=' + str(mid) + '&is_space=0&jsonp=jsonp'

	medialist_brief_jsonp_raw = requests.get(medialist_brief_jsonp).text
	wdata = json.loads(medialist_brief_jsonp_raw)
	medialist_count = wdata['data']['count']
	medialist = wdata['data']['list']

	medialist_brief.clear()
	for favlist_item in medialist:    
		fid = favlist_item['id']    
		title = favlist_item['title']    
		intro = favlist_item['intro'] 
		media_count = favlist_item['media_count']
		medialist_brief.append({'fid': fid, 'title': title, 'intro': intro, 'media_count': media_count})
		
		print(fid, title, media_count)

	medialist_brief
	# len(medialist_brief)

	############################
	# Each individual medialist
	medialist_detail = []
	for i in range(len(medialist_brief)):
		medialist_detail.append([])
	# print(len(medialist_detail))

	for serial in range(0, medialist_count, 1):
		fid = medialist_brief[serial]['fid']
		
		if medialist_brief[serial]['media_count'] % 20 != 0:
			page_num_max = int(medialist_brief[serial]['media_count'] / 20) + 1
		else:
			page_num_max = int(medialist_brief[serial]['media_count'] / 20)

		print('Folder %02d: %s' % (serial, medialist_brief[serial]['title']))
		for page_num in range(1, page_num_max + 1, 1):
			medialist_detail_jsonp = prefix + 'spaceDetail?media_id=' + str(fid) +'&pn=' + str(page_num) +'&ps=20&keyword=&order=mtime&type=0&tid=0&jsonp=jsonp'
			medialist_detail_raw = requests.get(medialist_detail_jsonp).text
			wdata = json.loads(medialist_detail_raw)
			medias = wdata['data']['medias']
			
			print('Page %02d' % (page_num))
			for fav_item in medias:    
				media_id = fav_item['id']    
				title = fav_item['title']    
				# intro = fav_item['intro'] 
				upper_mid = fav_item['upper']['mid']
				upper_name = fav_item['upper']['name']
				medialist_detail[serial].append({'media_id': media_id, 'upper_mid': upper_mid, 'intro': intro, 'upper_name': upper_name})
				
				print(media_id, upper_name, title)
			print('\n')

		medialist_detail_dump(medialist_detail[serial], medialist_title)

	return medialist_detail



def single_info_dump():
	fid = input('Medialist ID (aka fid): ')

	medialist_detail_jsonp = prefix + 'spaceDetail?media_id=' + str(fid) +'&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&jsonp=jsonp'
	medialist_detail_raw = requests.get(medialist_detail_jsonp).text
	wdata = json.loads(medialist_detail_raw)
	media_count = wdata['data']['info']['media_count']
	medialist_title = wdata['data']['info']['title']
	
	if media_count != 0:
		page_num_max = int(media_count / 20) + 1
	else:
		page_num_max = int(media_count / 20)

	medialist_detail = []
	for page_num in range(1, page_num_max + 1, 1):
		medialist_detail_jsonp = prefix + 'spaceDetail?media_id=' + str(fid) +'&pn=' + str(page_num) +'&ps=20&keyword=&order=mtime&type=0&tid=0&jsonp=jsonp'
		medialist_detail_raw = requests.get(medialist_detail_jsonp).text
		wdata = json.loads(medialist_detail_raw)
		medias = wdata['data']['medias']
			
		print('Page %02d' % (page_num))
		for fav_item in medias:    
			media_id = fav_item['id']    
			title = fav_item['title']    
			# intro = fav_item['intro'] 
			upper_mid = fav_item['upper']['mid']
			upper_name = fav_item['upper']['name']
			print(media_id, upper_name, title)
			
			medialist_detail.append({'media_id': media_id, 'title': title, 'upper_mid': upper_mid, 'upper_name': upper_name})
		print('\n')

	medialist_detail_dump(medialist_detail, medialist_title)
		
	return (medialist_detail, medialist_title)


def medialist_detail_dump(medialist_detail, medialist_title):

	o_metadata=open(r"./favlist_" + medialist_title + ".csv","w")
	print("Media_ID, Upper_ID, Upper_Name, Title", file = o_metadata)
	
	for i in range(len(medialist_detail)):
		print("av%s, %s, %s, %s" % (medialist_detail[i]['media_id'], medialist_detail[i]['upper_mid'], medialist_detail[i]['upper_name'], medialist_detail[i]['title']), file = o_metadata)

	print("Done.\nMetadata File has been created in your current dir.")
	o_metadata.close()


def file_dump(item_list, dump_mode, cookie_path, output_path, title = ""):

	# f_cookies = open(r"./myBilibiliCookies.txt","r")
	# cookies = f_cookies.read()
	# f_cookies.close()

	favlist_title = "favlist_" + title + ".csv"
	os.system('mv "%s" "%s"' % (favlist_title, output_path))
	output_path = os.path.join(os.path.expanduser(output_path), title)
	mkdir(output_path) 
	
	thread_amount = 15

	if cookie_path == '0':
		for media_item in item_list: 
			folder_basename = media_item['upper_name']
			folder_path = os.path.join(os.path.expanduser(output_path), folder_basename)
			mkdir(folder_path)
			os.system('annie -n %d -o "%s" -p av%d' % (thread_amount, folder_path, media_item['media_id']))
			# ffmpeg_repack(folder_path, media_item['title'])
			print("---  " + media_item['title'] + " Complete  ---\n")
	else:
		for media_item in item_list: 
			folder_basename = media_item['upper_name']
			folder_path = os.path.join(os.path.expanduser(output_path), folder_basename)
			mkdir(folder_path)
			os.system('annie -n %d -c "%s" -o "%s" -p av%d' % (thread_amount, cookie_path, folder_path, media_item['media_id']))
			# ffmpeg_repack(folder_path, media_item['title'])
			print("---  " + media_item['title'] + " Complete  ---\n")



# def ffmpeg_repack(folder_path, title):
	
# 	media_basename = os.path.join(os.path.expanduser(folder_path), title)
# 	media_input = media_basename + '.flv'
# 	media_output = media_basename + '.mp4'
# 	stream = ffmpeg.input(media_input)
# 	stream = ffmpeg.output(stream, media_output, **{'c': 'copy', 'movflags': '+faststart'})
# 	ffmpeg.run(stream)



def mkdir(path):
	
	folder = os.path.exists(path)
	if not folder:                   
		os.makedirs(path)            
		print("---  Made New Dir  ---")
	else:
		print("---  Alredy Exsits  ---")



def __main__():
	dump_mode = input("\nPlease Choose Mode:\n 1 --- Dump Single Folder\n 2 --- Dump All\nMode: ")

	cookie_path = input('Cookies Path (0 for not required): ')
	output_path = input('Output Path: ')

	if dump_mode == '1':
		medialist_info_set = single_info_dump()
		medialist_detail = medialist_info_set[0]
		medialist_title = medialist_info_set[1]
		file_dump(medialist_detail, dump_mode, cookie_path, output_path, title = medialist_title)
	
	elif dump_mode == '2':
		medialist_detail = all_info_dump()
		serial = 0
		for medialist in medialist_detail: 
			title = medialist_brief[serial]['title']
			file_dump(medialist_detail[serial], dump_mode, cookie_path, output_path, title = title)
			serial += 1

	print('All Complete')

__main__()





