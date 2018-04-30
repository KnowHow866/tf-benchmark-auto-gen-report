
# tf-benchmark-auto-gen-report

```
bash lab.sh resnet50 && bash lab.sh vgg16 && bash lab.sh alexnet&& bash lab.sh inception3
cd app

// run index.py it will parse tf-benchmark format to csv format and save to ./data
python index.py

// run plot.py and choose csv file to generate report, you can see in ./report
python plot.py
```