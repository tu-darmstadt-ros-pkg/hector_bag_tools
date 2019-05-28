#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK
from __future__ import print_function, division

import argparse
import argcomplete
from shutil import copyfile
import os

import rosbag
import rospy


def parse_arguments():
    parser = argparse.ArgumentParser(description='Merge static tf from one bag file to multiple others.')
    parser.add_argument('ref_bag', metavar='REF_BAG', help='Bagfile containing /static_tf')
    parser.add_argument('bags', metavar='BAGS', nargs="+", help='Target bag files')
    parser.add_argument("--publish_period", type=float, default=5.0, help="Desired publishing period of tf "
                                                                          "messages in s.")
    parser.add_argument("--no_backup", action="store_true", default=False, help="Disable creating of backup files")

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    return args


def get_static_tf(bag):
    tf_list = []
    for topic, msg, t in bag.read_messages(topics=['/tf_static']):
        tf_list.append(msg)
    return tf_list


def frange(start, stop, step):
    n = start
    while n < stop:
        yield n
        n += step


def backup(bag_path):
    filename = os.path.splitext(bag_path)[0]
    ext = os.path.splitext(bag_path)[1]

    backup_path = filename + '.orig' + ext

    if os.path.exists(backup_path):
        print("Backup file '{}' already exists. Skipping bag file.".format(backup_path))
        return False
    else:
        try:
            copyfile(bag_path, backup_path)
        except:
            print("Failed to create backup '{}'. Skipping bag file.".format(backup_path))
            return False
        else:
            return True


def write_tf_to_bag(bag, msg_list, period):
    start_time = bag.get_start_time()
    end_time = bag.get_end_time()
    for time in frange(start_time, end_time, period):
        write_time = rospy.Time(time)
        for msg in msg_list:
            bag.write("/tf_static", msg, write_time)


if __name__ == "__main__":
    args = parse_arguments()

    # Open reference bag
    print("Opening reference bag '{}'".format(args.ref_bag))
    ref_bag = rosbag.Bag(args.ref_bag, "r")
    tf_msgs = get_static_tf(ref_bag)
    print("Found {} tf messages".format(len(tf_msgs)))
    ref_bag.close()

    # Open target bags
    for bag_path in args.bags:
        print("Writing to bag '{}'".format(bag_path))
        if args.no_backup or backup(bag_path):
            bag = rosbag.Bag(bag_path, "a")
            write_tf_to_bag(bag, tf_msgs, args.publish_period)
            bag.close()






