# import traceback
# import os
# import copy
# from compose.cli.command import get_client as get_docker_client_no_tls
# def get_docker_client(host=None):
#     env = copy.deepcopy(os.environ)
#     env['COMPOSE_HTTP_TIMEOUT'] = "600"
#     if 'DOCKER_TLS_VERIFY' in env:
#         del env['DOCKER_TLS_VERIFY']
#     if 'DOCKER_CERT_PATH' in env:
#         del env["DOCKER_CERT_PATH"]
#     try:
#         client = get_docker_client_no_tls(env,
#                                           host=host,
#                                           version="1.25")
#     except Exception as e:
#         raise Exception("Get docker client error.e=%s,docker_host=%s"%(traceback.format_exception(e),host))
#
#     host = '127.0.0.1:8083'
#     print(get_docker_client(host))
#
#
a = [4,3,2,1]
# for i in range{len}:
#     print()
#     print(i.real)
