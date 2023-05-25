import glob
import time

import serial
import logging
import subprocess
import os
import os.path
import argparse
import datetime

CMD_READ_FLASH_SIZE = 'st-info --probe'
CMD_RESET_STM = 'st-flash reset'
CMD_READ_FLASH = 'st-flash read /home/user/Downloads/rb_discovery.bin 0x8000000 262144'
CMD_WRITE_FLASH = 'st-flash write /home/user/Downloads/rb_discovery.bin 0x8000000'
CMD_CLEAN_FLASH = 'st-flash erase'
#flash_size = 2048

def udev_query(dev):
    cmd = 'udevadm info -x -q all'.split() + [dev]
    logging.debug('running "%s"', ' '.join(cmd))
    out = subprocess.check_output(cmd, encoding='utf-8')
    return [l.strip() for l in out.strip().split('\n')]

def detect_stlink():
    ID_MODEL = 'E: ID_MODEL=STM32_STLink'
    usb_uarts = glob.glob('/dev/stlinkv2*')
    candidates = []
    for dev in usb_uarts:
        info = udev_query(dev)
        if ID_MODEL in info:
            logging.info('STLink  detect!')
            candidates.append(dev)
        else:
            logging.debug('STLink  not found')

    if len(candidates)==0:
        logging.error('No STLink have been found')
        raise RuntimeError('No STLink have been found')
    elif len(candidates) > 1:
        logging.error('STLink have been found')
        raise  RuntimeError('Many_STLink')
    else:
        logging.info(f'STLink have been found {dev}')
        print('STLink have been found')


def reset():
    cmd = CMD_RESET_STM.split()
    answ = subprocess.call(cmd)
    if (answ == 0):
        print("Reset!")


def erase():
    cmd = CMD_CLEAN_FLASH.split()
    answ = subprocess.call(cmd)
    if (answ == 0):
        print("Erase complete!")

def flash_size():
    cmd = CMD_READ_FLASH_SIZE.split()
    answer = str(subprocess.check_output(cmd)).split()
    arr = []
    for t in answer:
        arr.append(t)
    flash_size = arr[9]
    return flash_size

def read_flash():
    ts = time.perf_counter()
    date_now = datetime.datetime.now()
    cmd = CMD_READ_FLASH.split()
    cmd[2] += str(date_now)
    cmd[4] = flash_size()
    answ = subprocess.call(cmd)
    if (answ == 0):
        logging.debug("Done")
    else:
        logging.error('')
    all_time = time.perf_counter() - ts
    print(f'Successfully completed reading in {round(all_time, 2)} sec')

def write_flash():
    ts = time.perf_counter()
    cmd = CMD_WRITE_FLASH.split()
    answ = subprocess.call(cmd)
    if (answ == 0):
        logging.debug("Done")
    else:
        logging.error('')
    logging.debug("")
    reset()
    all_time = time.perf_counter()-ts
    print(f'Successfully completed flashing in {round(all_time,2)} sec')
def main():
    parser = argparse.ArgumentParser(description="STM test and flashing")
    parser.add_argument('-t', '--tty', help='Select ttyUSB')
    parser.add_argument('-r', '--read', help='Make backup')
    parser.add_argument('-f','--full', help='Backup, Erase and Write')
    parser.add_argument('-n','--name', help='Path', default='auto')
    args = parser.parse_args()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    detect_stlink()
    read_flash()





