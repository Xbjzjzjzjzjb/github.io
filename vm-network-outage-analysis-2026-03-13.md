# 虚拟机断网原因分析

日期: 2026-03-13

## 结论

这次“虚拟机断网”不是单一 DNS 污染，也不是 VirtualBox 网卡本身彻底断开，而是三层问题叠加：

1. 宿主机 `192.168.1.4:9910` 对虚拟机不可用。
   宿主机代理只监听在 `127.0.0.1:9910`，没有监听 `0.0.0.0:9910` 或 `192.168.1.4:9910`，也没有可用的 `portproxy`。因此虚拟机访问宿主机 `9910` 必然失败。

2. 虚拟机内 `Geph 9910` 处于“端口在监听，但代理转发不正常”的状态。
   实测通过 `127.0.0.1:9910` 访问 `example.com` 和 `chatgpt.com` 时都出现 `Connection reset by peer`。更早的探测里还出现过 `HTTP/1.1 500 Internal Server Error` 和 `Relay failed to example.com:80`，说明并不是端口没开，而是代理核心或上游链路异常。

3. 虚拟机内 `V2Ray 10809` 一度可用，但在后续复测时也出现 TLS 握手异常。
   早期测试曾验证 `127.0.0.1:10809` 可正常访问 `example.com`，访问 `chatgpt.com` 返回 `HTTP 403 challenge`，这更像 Cloudflare 挑战而不是物理断网。后续复测中，`10809` 又出现 `HTTP/1.1 200 Connection established` 后紧接 `unexpected eof while reading`，说明代理核心状态后来也变得不稳定。

## 决定性原因

如果只追问“为什么你感觉虚拟机总掉线”，决定性原因不是网卡有没有 IP，而是你在混用两条不稳定或不可达的代理路径：

- 一条是根本没有对虚拟机开放的宿主机 `9910`
- 一条是虚拟机内虽然监听但经常重置连接的 `Geph 9910`

后续连 `V2Ray 10809` 也出现 TLS 异常，进一步说明问题已经从“代理配置不对”扩大到“代理程序本身状态异常或上游链路不稳定”。

## 排除项

- 不是 `sshd` 没开。宿主机到虚拟机 `192.168.1.144:22` 可达。
- 不是 VirtualBox NAT/桥接切换导致当天所有代理都失效。虚拟机本机代理端口曾经存在监听。
- 不是单纯 DNS 污染。`10809` 可建立 HTTP CONNECT，而后续失败发生在 TLS 或代理转发阶段。

## 直接建议

- 不要再依赖宿主机 `192.168.1.4:9910`，除非宿主机代理显式开启 `Allow LAN` 或监听到 `0.0.0.0`。
- 不要混用多个代理入口做日常出口，先固定一种并持续验证。
- 优先重启并单独验证虚拟机内代理程序，再决定保留 `Geph 9910` 还是 `V2Ray 10809`。

## 关键证据摘录

- 宿主机只有 `127.0.0.1:9910`，没有 `0.0.0.0:9910`、`192.168.1.4:9910`。
- `Geph 9910`:
  - `example.com -> Connection reset by peer`
  - `chatgpt.com -> Connection reset by peer`
  - 早期还出现 `Relay failed to example.com:80`
- `V2Ray 10809`:
  - 早期: `example.com` 正常，`chatgpt.com` 返回 `HTTP 403 challenge`
  - 后期: `HTTP/1.1 200 Connection established` 后报 `unexpected eof while reading`
