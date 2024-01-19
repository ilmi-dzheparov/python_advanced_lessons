import logging

root_logger = logging.getLogger()
# logging.basicConfig(level=logging.DEBUG)
module_logger = logging.getLogger('module_logger')
submodule_logger = logging.getLogger('module_logger.submodwle_logger')
# module_logger.setLevel('DEBUG')

formatter = logging.Formatter(
    fmt='%(name)s || %(levelname)s || %(message)s || %(module)s.%(funcName)s:%(lineno)s'
)
module_handler = logging.StreamHandler()
print(module_handler.level)
module_handler.setLevel("INFO")

module_handler.setFormatter(formatter)
# module_handler.setLevel("INFO")
module_logger.addHandler(module_handler)
module_logger.propagate = False
# module_logger.setLevel("INFO")
print(module_logger.level)



def main():
    print('Root logger:')
    print(root_logger.handlers)
    print('Module_logger:')
    print(module_logger.handlers)
    module_logger.info("message")
    print('Submodule_logger:')
    print(submodule_logger.handlers)

if __name__ == "__main__":
    main()