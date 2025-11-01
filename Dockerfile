FROM python:3.12-slim

ARG REGISTRY

RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

RUN mkdir /webApp
WORKDIR /webApp

COPY ./ ./

RUN adduser --system --home /home/security_business_notice --group --uid 1000 security_business_notice 
RUN mkdir -p /home/security_business_notice && chown security_business_notice:security_business_notice /home/security_business_notice

RUN chown -R security_business_notice:security_business_notice .
RUN chmod -R 744 .

USER security_business_notice

# PATH 환경변수 수정
ENV PATH="${PATH}:/home/security_business_notice/.local/bin"

RUN pip3 install --extra-index-url ${REGISTRY} -r requirements.txt

CMD ["python3", "main.py"]