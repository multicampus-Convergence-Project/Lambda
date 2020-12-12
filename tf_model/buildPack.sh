# 기본 패키지 최신 업데이트
# python 3.7 버전 설치
# 기타 패키지 설치
dev_install() {
    yum -y update
    yum -y upgrade
    yum install -y \
    wget \
    gcc \
    gcc-c++ \
    cmake \
    zlib-devel \ 
    zip
    echo "dev_install done..."
    # unzip \
    # blas-devel lapck-devel atlas-devel
}
# 가상환경 생성
mkvirtualenvs() {
    cd /home/
    rm -rf venv
    python3 -m venv venv
    source venv/bin/activate
    echo "mkvirtualenvs done..."
    # text="
    # [global]
    # index-url=http://ftp.daumkakao.com/pypi/simple
    # trusted-host=ftp.daumkakao.com
    # "
    # echo "$text" > $VIRTUAL_ENV/pip.conf 
    # echo "UNDER: pip.conf ==="
    # cat $VIRTUAL_ENV/pip.conf
}

pip_install() {
    # source /home/venv/bin/activate
    pip install -U pip wheel
    # 의존 패키지 설치 x / 해당 패키지 설치
    pip install tensorflow --no-deps
    # pip install h5py
    # pip install pandas
    pip install pillow
    deactivate
}

gather_pack() {
    cd /home/ && rm -rf pack && mkdir pack && cd pack
    cp -R /home/venv/lib/python3.7/site-packages/* .
    cp -R /home/venv/lib64/python3.7/site-packages/* .

    cp /outputs/modelload.py /home/pack/modelload.py

    find . -type d -name "test" -exec rm -rf {} +
    find -name "*.so" | xargs strip
    find -name "*.so.*" | xargs strip

    rm -r pip && rm -r pip-* && rm -r wheel && rm -r wheel-*
    find . | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf
    echo "stripped size $(du -sh /home/pack | cut -f1)"

    zip -FS -r1 /outputs/pack.zip * > /dev/null
    echo "compressed size $(du -sh /outputs/pack.zip | cut -f1)"
}

main() {
    dev_install
    mkvirtualenvs
    pip_install
    gather_pack
}

main