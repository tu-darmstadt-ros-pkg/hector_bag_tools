# hector_bag_tools
Scripts for processing bag files.

## split_bag
Usage: 

`rosrun hector_bag_tools split_bag.py [--duration --size --repeat_latched] bagfile`

Either the `--duration` (seconds) or `--size` (GB) argument is required.
If the flag `--repeat_latched` is set, all messages that were sent via a latched connection are written to each new bag file.
This can be useful for tf_static messages.
