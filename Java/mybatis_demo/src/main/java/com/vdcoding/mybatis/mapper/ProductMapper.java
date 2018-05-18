package com.vdcoding.mybatis.mapper;

import java.util.List;
import org.apache.ibatis.annotations.Select;
import org.apache.ibatis.annotations.Update;
import com.vdcoding.mybatis.pojos.Product;

public interface ProductMapper {
	@Select("select * from product")
	public List<Product> getAllProduct();
	
	@Select("select * from product where id=#{id}")
	public Product getProductById(int id);
	
	@Update("update product set productname=#{productname},price=#{price} where id=#{id}")
	int updateProduct(Product product);
}
