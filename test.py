import vk_api

vk_session = vk_api.VkApi('+79995337015', 'Sergeev691061')
vk_session.auth()

vk = vk_session.get_api()

print(vk.wall.post(message='Hello world!'))