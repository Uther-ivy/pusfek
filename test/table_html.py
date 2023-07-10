def doc_html():
    htmldata += f'''
                    <tbody>
                            <th>{toubiaoren}</th>
                            <th>{biaoduan}</th>
                            <th>{biaoduanbaojia}</th>
                            <th>{jishufen}</th>
                            <th>{shangwufen}</th>
                            <th>{jiagefen}</th>
                            <th>{pingbiaozongfen}</th>
                            <th>{paiming}</th>
                   </tbody>   
                '''
    html = f"""
                <div>
                    <table border="='0.5" width="70%">
                        <p class="pj">招标投标项目名称:{toubiaomingcheng}</p>
                        <p class="jg">招标代理机构：{zhaobiaojigou}</p>
                        <tbody>
                            <td >投标人</td>
                            <td>标段	</td>
                            <td>标段报价(元)	</td>
                            <td>技术分</td>
                            <td>商务分</td>
                            <td>价格分</td>
                            <td>评标总分</td>
                            <td>排名</td>
                            <td>备注</td>
                        </tbody>
                            {htmldata}

                    </table>
                    <p>公示日期：{gongshiriqi}</p>
                    <p>公示结束日期：{gongshijieshuriqi}</p>
                    <p>联系人：{lianxiren}</p>
                    <p>代理机构电话：{dianhua}</p>

    </div>
            """
