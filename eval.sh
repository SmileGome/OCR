# 100k로만 학습한 모델 : original_test - BLEU 약 0.7
python -m eval --config C:\GOME\pix2tex\pix2tex\model\settings\config.yaml --data C:\GOME\pix2tex\pix2tex\dataset\data\original\test.pkl
python -m eval --checkpoint C:\GOME\pix2tex\pix2tex\checkpoints\50k_crawled\50k_crawled_e01_step5999.pth --config C:\GOME\pix2tex\pix2tex\model\settings\config50.yaml --data C:\GOME\pix2tex\pix2tex\dataset\data\50K\test50k.pkl
# 50k 추가학습 모델 : 50k_test - BLEU 약 0.6, original_test - 쓰레기 
python -m eval --checkpoint C:\GOME\pix2tex\pix2tex\checkpoints\50k_crawled\50k_crawled_e01_step5999.pth --config C:\GOME\pix2tex\pix2tex\model\settings\config.yaml --data C:\GOME\pix2tex\pix2tex\dataset\data\original\test.pkl
# => 추가 데이터를 resize한 후 추가학습하는 실험해바야지~