# 功能预期
!!! note "项目目标"
    减少使用Sap2000计算和验算过程中的重复操作，提高横向项目的工作效率。

- [x] CSI OAPI的基本使用
- [x] 简单桥梁模型的建立
    - [x] 主梁
    - [ ] 支座:
        - [x] 理想支座
        - [x] MultiLinearElastic(注意此支座无滞回性质，本构曲线原路返回)
        - [x] PlasticWen(摩擦摆，钢阻尼器等)
    - [ ] 桥墩:
        - [ ] 均匀自定义墩(建议用户自行实现)
        - [x] 箱墩
        - [ ] 其他常见的墩
    - [ ] 基础:
        - [x] 六弹簧
        - [ ] Winkler地基梁
- [x] 工况设置、分组、计算
    - [x] 反应谱函数，阻尼比，方向，工况定义，从txt读取反应谱等功能，详见`SapEarthquake.Spectrum`类及`SapEarthquake.SapSpectrumCase`类
    - [x] 时程函数，阻尼比，方向，工况定义，支持直接积分法（DirTH）和模态叠加法（Modal），详见`SapEarthquake.SapTimeHistoryFunc`类及`SapEarthquake.SapModalTimeHistoryCase`类
    - [x] 将节点，单元，link等添加到指定组（Group）,详见`Sap.Scripts.Group`类
    - [x] 提取结果时选择指定组别，详见`Saproject.Scripts.SelectCombo_Case`方法
    - [x] 选择工况并计算，计算失败时可以自动重算，详见`Saproject.Scripts.Analyze`类
- [x] 结果提取，输出至Excel
- [ ] 自动进行截面验算，给出建议配筋率
- [ ] 自动生成报告

---

# 参考资料
- 官方API文档来自于Sap2000安装目录中的[CSI_OAPI_Documentation.chm](../CSI_OAPI_Documentation.chm)(这里给出的是v25版本)
- 部分代码重构自[郭军军](https://github.com/Junjun1guo)的项目[pythonInteractSAP2000](https://github.com/Junjun1guo/pythonInteractSAP2000)

!!! info "开源协议"
    本项目遵循GPL-3.0 license开源协议，欢迎大家提出建议和贡献代码。
