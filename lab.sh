
#!/bin/bash

model=resnet50
if [ ! -z $1 ]; then
    model=$1
fi
echo -e "Model: ${model}"
mkdir app/raw-data
mkdir app/raw-data/$model
mkdir app/raw-data/$model-training

batch=(1 2 4 8 10 16 20 25 32)

for ((i=0; i<${#batch[@]}; i++)); do
    # cpu 
    python tf_cnn_benchmarks.py --device=cpu --data_format=NHWC --model=$model --variable_update=parameter_server  --batch_size=${batch[$i]} > report/app/raw-data/$model-training/gpu-$model-b${batch[$i]}.txt
    
    # GPU
    python tf_cnn_benchmarks.py --num_gpus=1 --model=$model --variable_update=parameter_server  --batch_size=${batch[$i]} > app/raw-data/$model-training/gpu-$model-b${batch[$i]}.txt
    wait
    python tf_cnn_benchmarks.py --num_gpus=1 --model=$model --variable_update=parameter_server --forward_only=True --batch_size=${batch[$i]} > app/raw-data/$model/gpu-$model-b${batch[$i]}.txt
    wait
    python tf_cnn_benchmarks.py --num_gpus=1 --model=$model --variable_update=parameter_server --forward_only=False --batch_size=${batch[$i]} > rapp/raw-data/$model-back/gpu-$model-b${batch[$i]}.txt
    wait
    echo -e "bact-size ${batch[$i]} done"
done

exit 0
